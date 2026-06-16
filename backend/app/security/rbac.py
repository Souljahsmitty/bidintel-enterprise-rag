"""Role-based access control. Maps a role to the document access-groups it may read.
Enforcement rule: every retrieval is filtered by tenant_id AND allowed access groups
BEFORE any chunk reaches the model context."""

ROLE_GROUPS = {
    "proposal_writer":   ["proposal", "past_performance", "public"],
    "capture_manager":   ["proposal", "past_performance", "capture", "pricing", "public"],
    "contracts_manager": ["contract", "compliance", "proposal", "public"],
    "executive_reviewer":["summary", "proposal", "past_performance", "public"],
    "auditor":           ["audit", "summary", "public"],
    "hr":                ["hr"],
    "system_admin":      ["*"],
}

def allowed_groups(role: str):
    return ROLE_GROUPS.get(role, ["public"])

def can_access(role: str, group: str) -> bool:
    groups = allowed_groups(role)
    return "*" in groups or group in groups

def sql_filter(role: str):
    """Returns (clause, params) to AND into retrieval SQL. Admin gets no extra filter."""
    groups = allowed_groups(role)
    if "*" in groups:
        return ("", [])
    return ("AND access_groups && %s::text[]", [groups])
