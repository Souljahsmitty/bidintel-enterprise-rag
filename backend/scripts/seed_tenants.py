from app.database import get_conn
from app.services.tenant_service import DEMO_TENANT_ID
with get_conn() as c, c.cursor() as cur:
    cur.execute("INSERT INTO tenants (id,name) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (DEMO_TENANT_ID, "demo"))
print("seeded demo tenant")
