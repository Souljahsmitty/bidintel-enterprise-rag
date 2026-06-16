import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:bidintel@localhost:5432/postgres")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "mock-claude")
MAX_RAG_RETRIES = int(os.getenv("MAX_RAG_RETRIES", "2"))
EMBED_DIM = 384
