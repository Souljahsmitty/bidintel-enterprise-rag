DEMO_TENANT_ID = "00000000-0000-0000-0000-000000000001"


def normalize_tenant_id(tenant_id: str | None) -> str:
    if not tenant_id or tenant_id == "demo":
        return DEMO_TENANT_ID
    return tenant_id
