# BidIntel — Directory Structure

```text
bidintel/
├── README.md                      # what it is, simulated-vs-production, quick start, proof
├── STRUCTURE.md                   # this file
├── docker-compose.yml             # db (pgvector) + backend + frontend
├── .env.example                   # config template, no secrets
├── .github/
│   └── workflows/
│       └── bidintel-ci.yml        # CI: tests, frontend build, docker build
├── scripts/
│   └── start_local.sh             # one-command: containers -> migrate -> seed -> URLs
├── docs/
│   ├── architecture/
│   │   ├── bidintel-enterprise-architecture.mmd   # Mermaid diagram
│   │   └── bidintel-enterprise-architecture.md
│   ├── aws_iam_simulation.md       # simulated AWS (IAM, Bedrock, hosting)
│   ├── aws_bedrock_simulation.md
│   ├── aws_hosting_simulation.md
│   ├── BACKUP_RESTORE_RUNBOOK.md
│   ├── HIRING_MANAGER_DEMO_SCRIPT.md
│   └── screenshots/                # (add real run screenshots here)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── create_tables.sql       # base schema (tables, vector+keyword cols, indexes, trigger)
│   │   ├── seed_mock_corpus.py     # 5 mock federal docs
│   │   ├── test_access_control.py  # RBAC proof
│   │   └── test_full_pipeline.py
│   ├── tests/
│   │   └── evals/
│   │       ├── test_rag_quality.py # RAGAS-style regression tests
│   │       └── eval_dataset.jsonl
│   └── app/
│       ├── main.py                 # FastAPI app; includes every router
│       ├── config.py               # env settings
│       ├── database.py             # Postgres connection + pgvector register
│       ├── api/                    # ── URL routes (one screen action each)
│       │   ├── upload_routes.py     # POST /upload
│       │   ├── ask_routes.py        # POST /ask  (RAG + evaluation pipeline)
│       │   ├── scoring_routes.py    # POST /score-proposal
│       │   ├── feedback_routes.py   # POST /feedback
│       │   ├── compliance_routes.py # GET  /compliance/{id}
│       │   ├── dashboard_routes.py  # GET  /dashboard
│       │   ├── audit_routes.py      # GET  /audit-logs
│       │   └── health_routes.py     # GET  /health
│       ├── security/
│       │   └── rbac.py              # role -> allowed access groups; SQL filter
│       ├── database/
│       │   └── migrations/
│       │       └── 003_enterprise_tables.sql   # roles, eval_runs/scores, citation_checks, etc.
│       ├── rag/
│       │   ├── evaluate.py          # grounded-ness verdict (PASS/FAIL)
│       │   └── retry_policy.py      # retry routing
│       └── services/               # ── one file = one pipeline stage
│           ├── pdf_loader.py        # PDF -> text per page
│           ├── text_cleaner.py      # normalize text
│           ├── chunker.py           # overlapping chunks
│           ├── embedding_service.py # text -> 384-dim vector (local MiniLM)
│           ├── store.py             # write chunks + vectors
│           ├── bm25_service.py      # keyword search (RBAC-filtered)
│           ├── vector_search_service.py  # meaning search (RBAC-filtered)
│           ├── rrf_fusion_service.py     # combine rankings
│           ├── hybrid_search_service.py  # bm25 + vector -> RRF
│           ├── reranker_service.py       # cross-encoder rerank
│           ├── context_builder.py        # grounded prompt
│           ├── bedrock_llm_service.py    # (mock) LLM -> real Bedrock swap
│           ├── citation_service.py       # [n] -> doc/page/chunk
│           ├── proposal_scoring_service.py
│           ├── audit_service.py
│           ├── document_versioning_service.py  # hash -> version -> deactivate old chunks
│           ├── access_control.py
│           ├── evaluation/
│           │   ├── citation_verifier.py      # does each citation support the claim?
│           │   ├── response_score_service.py # user-facing Response Quality score
│           │   ├── ragas_service.py          # (sim) RAGAS/DeepEval metrics
│           │   └── phoenix_service.py        # (sim) tracing spans
│           └── observability/
│               └── request_logger.py         # latency + token + cost -> request_logs
└── frontend/
    ├── Dockerfile                  # build React, serve static
    ├── package.json
    ├── plain/                      # ── the full site as plain HTML/CSS/JS (no build step)
    │   ├── login.html  dashboard.html  documents.html  assistant.html
    │   ├── compliance.html  bid.html  audit.html
    │   ├── styles.css  api.js  layout.js
    └── src/                        # ── the React version (components)
        ├── App.jsx
        ├── api/bidintelApi.js
        ├── components/  (UploadDocument, AskQuestion, AnswerPanel, EvidencePanel,
        │                 ProposalScoring, PipelineVisualizer, FeedbackButtons, Login)
        └── pages/
```

Generate this live anytime with:  `find . -type d -not -path '*/__pycache__*' | sort`
