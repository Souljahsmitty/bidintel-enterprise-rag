"""Run keyword + vector search (both RBAC-filtered), then fuse with RRF."""
from .bm25_service import bm25_search
from .vector_search_service import vector_search
from .rrf_fusion_service import rrf

def hybrid_search(cur, tenant_id, query, role="proposal_writer"):
    bm25 = bm25_search(cur, tenant_id, query, role)
    vec = vector_search(cur, tenant_id, query, role)
    return rrf(bm25, vec)
