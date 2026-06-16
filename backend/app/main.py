from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import upload_routes, ask_routes, scoring_routes, health_routes, feedback_routes, compliance_routes, dashboard_routes, audit_routes, documents_routes

app = FastAPI(title="BidIntel API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
for r in (health_routes, upload_routes, ask_routes, scoring_routes, feedback_routes, compliance_routes, dashboard_routes, audit_routes, documents_routes):
    app.include_router(r.router)
# run: uvicorn app.main:app --reload --port 8000
