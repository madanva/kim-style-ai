
from __future__ import annotations
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pgvector.sqlalchemy import Vector

PG_USER = os.getenv("POSTGRES_USER", "kim")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "kim_pass")
PG_DB   = os.getenv("POSTGRES_DB", "kimdb")
PG_HOST = os.getenv("POSTGRES_HOST", "postgres")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def init_db():
    with engine.begin() as conn:
        # Enable extension (Postgres 16 with 'vector' preloaded in compose)
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
