"""SIMULATED end-to-end BidIntel workflow — runs anywhere (no Docker, no model
downloads, no network). Uses the REAL modules for every stage; only the embedding
and reranker model calls are deterministic stand-ins (the same things mocked in prod).
Run:  cd backend && PYTHONPATH=. python scripts/sim_workflow.py"""
import re, math
from app.services.text_cleaner import clean
from app.services.chunker import chunk
from app.services.rrf_fusion_service import rrf
from app.services.context_builder import build_context
from app.services.citation_service import attach_citations
from app.services.evaluation.citation_verifier import verify_citations
from app.services.evaluation.ragas_service import evaluate_rag
from app.services.evaluation.response_score_service import response_quality
from app.services.evaluation.phoenix_service import trace
from app.rag.evaluate import evaluate
from app.security.rbac import allowed_groups, can_access

# ---- deterministic stand-in for the embedding model (no torch/network) ----
def mock_embed(text):
    v = [0.0]*64
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        v[hash(w) % 64] += 1.0
    n = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/n for x in v]
def cos(a,b): return sum(x*y for x,y in zip(a,b))

# ---- demo corpus (text + access group) ----
DOCS = [
 ("DHS RFP","proposal","The contractor shall provide 24/7 SOC monitoring services. FedRAMP Moderate authorization is required."),
 ("SOC Past Performance","past_performance","Delivered 24/7 SOC monitoring and reduced mean time to respond by 40 percent."),
 ("Compliance Policy","compliance","The contractor shall comply with NIST SP 800-171 and provide monthly metrics reporting."),
 ("HR Payroll (restricted)","hr","Employee payroll records and salary bands. Restricted to HR only."),
]

def ingest():
    store=[]; cid=0
    print("\n=== STAGE 1-5  INGESTION ===")
    for title,group,text in DOCS:
        for piece in chunk(clean(text), size=120, overlap=20):
            cid+=1
            store.append({"id":cid,"doc":title,"group":group,"text":piece,"vec":mock_embed(piece)})
        print(f"  loaded+cleaned+chunked+embedded+stored: {title:24s} [{group}]")
    print(f"  -> {len(store)} chunks in the (in-memory) store")
    return store

def search(store, query, role):
    groups=allowed_groups(role)
    # RBAC filter BEFORE retrieval
    visible=[c for c in store if ("*" in groups or c["group"] in groups)]
    qtokens=set(re.findall(r"[a-z0-9]+", query.lower()))
    bm25=sorted(((c["id"],c["text"],len(qtokens & set(re.findall(r"[a-z0-9]+",c["text"].lower())))) for c in visible),
                key=lambda r:-r[2])[:5]
    qv=mock_embed(query)
    vec=sorted(((c["id"],c["text"],cos(qv,c["vec"])) for c in visible), key=lambda r:-r[2])[:5]
    return bm25, vec, {c["id"]:c for c in visible}

def ask(store, question, role):
    print(f"\n=== ASK  ('{question}'  as role={role}) ===")
    trace("question", question)
    bm25, vec, byid = search(store, question, role)
    print(f"  STAGE 6  RBAC filter: role {role} may read {allowed_groups(role)}")
    print(f"  STAGE 7  BM25 keyword hits : {[r[0] for r in bm25]}")
    print(f"  STAGE 8  vector hits       : {[r[0] for r in vec]}")
    fused = rrf(bm25, vec)
    print(f"  STAGE 9  RRF fused ids     : {[f['id'] for f in fused]}")
    # deterministic 'rerank' = keyword overlap with the question, keep top 2
    qtokens=set(re.findall(r"[a-z0-9]+", question.lower()))
    for f in fused:
        f["rerank"]=len(qtokens & set(re.findall(r"[a-z0-9]+", f["text"].lower())))
    top=sorted(fused,key=lambda f:-f["rerank"])[:2]
    if not top:
        print("  RESULT: no allowed evidence -> answer abstains (correct for blocked role).")
        return
    ev=[{"id":t["id"],"text":t["text"],"doc":byid[t["id"]]["doc"],"page":1,"file":byid[t["id"]]["doc"]} for t in top]
    print(f"  STAGE 10 rerank -> top chunks: {[e['id'] for e in ev]}")
    ctx=build_context(question, ev)
    # mock LLM answer grounded in the top chunks
    answer=" ".join(f"{ev[i]['text']} [{i+1}]" for i in range(len(ev)))
    print(f"  STAGE 11 context built ({len(ctx)} chars) -> STAGE 12 mock Bedrock answer:")
    cited=attach_citations(answer, ev)
    print(f"           ANSWER: {cited['answer'][:160]}...")
    print(f"  STAGE 13 citations: {[(c['marker'],c['filename']) for c in cited['citations']]}")
    ver=verify_citations(cited["answer"], cited["citations"])
    m=evaluate_rag(question, cited["answer"], ev); m["citation_accuracy"]=ver["citation_accuracy"]; m["sources_used"]=len(ev)
    q=response_quality(m)
    print(f"  STAGE 14 citation_accuracy={ver['citation_accuracy']}  faithfulness={m['faithfulness']}")
    print(f"  STAGE 15 RESPONSE QUALITY: {q['response_quality']}%  | support={q['citation_support']} "
          f"| coverage={q['evidence_coverage']} | risk={q['hallucination_risk']} | sources={q['sources_used']}")
    print(f"  STAGE 16 evaluator verdict: {evaluate(cited['answer'], ev)['verdict']}  -> audit logged")

if __name__=="__main__":
    print("BIDINTEL — SIMULATED END-TO-END WORKFLOW (no Docker / no network)")
    store=ingest()
    ask(store, "What is the SOC monitoring requirement?", "proposal_writer")
    ask(store, "Show me the payroll records", "proposal_writer")  # RBAC should block HR
    ask(store, "Show me the payroll records", "hr")               # HR allowed
    print("\nDONE — ingestion -> retrieval -> RBAC -> RRF -> rerank -> context -> answer -> citations -> evaluation.")
