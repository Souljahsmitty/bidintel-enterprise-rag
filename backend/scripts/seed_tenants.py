from uuid import uuid4
from app.database import get_conn
with get_conn() as c, c.cursor() as cur:
    cur.execute("INSERT INTO tenants (id,name) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                (uuid4(), "demo"))
print("seeded demo tenant")
