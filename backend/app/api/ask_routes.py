"""POST /ask — RAG + enterprise evaluation:
hybrid (RBAC-filtered) -> rerank -> context -> generate -> cite -> verify citations ->
RAGAS metrics -> response-quality score -> store evaluation_run/scores -> request log."""
from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel
from ..database import get_conn
from ..services.hybrid_search_service import hybrid_search
from ..services.reranker_service import rerank
from ..services.context_builder import build_context
from ..services.bedrock_llm_service import generate
from ..services.citation_service import attach_citations
from ..services import audit_service
from ..services.evaluation.ragas_service import evaluate_rag
from ..services.evaluation.citation_verifier import verify_citations
from ..services.evaluation.response_score_service import response_quality
from ..services.evaluation.phoenix_service import trace
from ..services.observability.request_logger import Timer, log_request
from ..services.tenant_service import normalize_tenant_id
router = APIRouter()

class AskBody(BaseModel):
    question: str
    opportunity_id: str | None = None
    tenant_id: str = "demo"
    role: str = "proposal_writer"

@router.post("/ask")
def ask(body: AskBody):
    with Timer() as timer, get_conn() as c, c.cursor() as cur:
        tenant_id = normalize_tenant_id(body.tenant_id)
        trace("question", body.question)
        candidates = hybrid_search(cur, tenant_id, body.question, body.role)
        trace("retrieved", len(candidates))
        evidence = rerank(body.question, candidates)
        trace("reranked", len(evidence))
        context = build_context(body.question, evidence)
        gen = generate(context)
        cited = attach_citations(gen["answer"], evidence)
        # ---- enterprise evaluation ----
        metrics = evaluate_rag(body.question, cited["answer"], evidence)
        cite_check = verify_citations(cited["answer"], cited["citations"])
        metrics["citation_accuracy"] = cite_check["citation_accuracy"]
        metrics["sources_used"] = len(cited["citations"])
        quality = response_quality(metrics)
        trace("evaluated", quality["response_quality"])
        run_id = _store_eval(cur, body, tenant_id, cited["answer"], metrics, cite_check)
        audit_service.log(cur, tenant_id, "user", "ask",
                          query=body.question, eval=metrics["faithfulness"])
    log_after(body, timer, gen)
    return {"answer": cited["answer"], "citations": cited["citations"],
            "evidence": evidence, "eval": metrics, "quality": quality,
            "evaluation_run_id": str(run_id) if run_id else None, "model": gen["model"]}

def _store_eval(cur, body, tenant_id, answer, metrics, cite_check):
    try:
        run_id = uuid4()
        cur.execute("INSERT INTO evaluation_runs (id,question,answer,tenant_id) VALUES (%s,%s,%s,%s)",
                    (run_id, body.question, answer, tenant_id))
        cur.execute("""INSERT INTO evaluation_scores
            (evaluation_run_id,faithfulness,answer_relevance,context_precision,
             context_recall,citation_accuracy,response_quality)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (run_id, metrics["faithfulness"], metrics["answer_relevance"],
             metrics["context_precision"], metrics["context_recall"],
             metrics["citation_accuracy"], response_quality(metrics)["response_quality"]/100))
        for ch in cite_check["checks"]:
            cur.execute("""INSERT INTO citation_checks
                (evaluation_run_id,claim,citation,supported,reason) VALUES (%s,%s,%s,%s,%s)""",
                (run_id, ch["claim"], ch["citation"], ch["supported"], ch["reason"]))
        return run_id
    except Exception:
        return None  # enterprise tables not migrated yet; answer still returns

def log_after(body, timer, gen):
    try:
        with get_conn() as c, c.cursor() as cur:
            u = gen.get("usage", {})
            log_request(cur, None, "/ask", timer.ms, u.get("in", 0), u.get("out", 0))
    except Exception:
        pass
