import psycopg
from pgvector.psycopg import register_vector
from .config import DATABASE_URL

def get_conn():
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    register_vector(conn)
    return conn
