"""Exact-answer cache for repeated questions.

This is the first layer in the model efficiency harness: if the same tenant/role
asks the same normalized question again, return the verified stored answer and
skip retrieval/reranking/LLM generation.
"""
import hashlib
import re
from uuid import UUID
from psycopg.types.json import Jsonb


def normalize_question(question: str) -> str:
    cleaned = re.sub(r"\s+", " ", question.strip().lower())
    return cleaned.rstrip("?!. ")


def question_hash(question: str) -> str:
    return hashlib.sha256(normalize_question(question).encode("utf-8")).hexdigest()


def get_cached_answer(cur, tenant_id: str, role: str, question: str):
    cur.execute(
        """SELECT answer,citations,evidence,metrics,quality,source,confidence,hit_count
           FROM query_answer_cache
           WHERE tenant_id=%s AND role=%s AND question_hash=%s""",
        (tenant_id, role, question_hash(question)),
    )
    row = cur.fetchone()
    if not row:
        return None
    cur.execute(
        """UPDATE query_answer_cache
           SET hit_count = hit_count + 1, updated_at = now()
           WHERE tenant_id=%s AND role=%s AND question_hash=%s""",
        (tenant_id, role, question_hash(question)),
    )
    return {
        "answer": row[0],
        "citations": row[1] or [],
        "evidence": row[2] or [],
        "eval": row[3] or {},
        "quality": row[4] or {},
        "answer_source": "cache",
        "cached_from": row[5],
        "confidence": row[6],
        "cache_hit_count": (row[7] or 0) + 1,
        "model": "none-cache-hit",
    }


def _jsonable(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    return value


def store_answer(cur, tenant_id: str, role: str, question: str, payload: dict, source: str, confidence: float):
    cur.execute(
        """INSERT INTO query_answer_cache
           (tenant_id,role,question_hash,question,answer,citations,evidence,metrics,quality,source,confidence)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
           ON CONFLICT (tenant_id, role, question_hash) DO UPDATE SET
             answer=EXCLUDED.answer,
             citations=EXCLUDED.citations,
             evidence=EXCLUDED.evidence,
             metrics=EXCLUDED.metrics,
             quality=EXCLUDED.quality,
             source=EXCLUDED.source,
             confidence=EXCLUDED.confidence,
             updated_at=now()""",
        (
            tenant_id,
            role,
            question_hash(question),
            question,
            payload["answer"],
            Jsonb(_jsonable(payload.get("citations", []))),
            Jsonb(_jsonable(payload.get("evidence", []))),
            Jsonb(_jsonable(payload.get("eval", {}))),
            Jsonb(_jsonable(payload.get("quality", {}))),
            source,
            confidence,
        ),
    )
