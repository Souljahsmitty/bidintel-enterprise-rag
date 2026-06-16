import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:bidintel@localhost:5432/postgres")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "mock-claude")
MAX_RAG_RETRIES = int(os.getenv("MAX_RAG_RETRIES", "2"))
EMBED_DIM = 384
MODEL_EFFICIENCY_ENABLED = os.getenv("MODEL_EFFICIENCY_ENABLED", "true").lower() == "true"
TRUSTED_KB_DIRECT_ENABLED = os.getenv("TRUSTED_KB_DIRECT_ENABLED", "true").lower() == "true"
TRUSTED_KB_CONFIDENCE_THRESHOLD = float(os.getenv("TRUSTED_KB_CONFIDENCE_THRESHOLD", "0.68"))
