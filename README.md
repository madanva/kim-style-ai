
# Kim Style AI — MVP Starter

Minimal scaffold for the Phase 1 MVP: upload Kim references → crawl brands → embed → ANN rank → clean URLs → results.

## Quick start
```bash
# 1) Copy env and adjust passwords/keys
cp .env.example .env

# 2) Start services (Postgres + Redis + API + Worker)
docker compose up --build

# 3) Visit API docs
open http://localhost:8000/docs
```

> Notes
- Playwright scraping is stubbed; add brand-specific extractors in `src/crawler/brands/`.
- Embeddings use OpenCLIP by default; switch in `src/app/embeddings.py`.
- Vector search uses pgvector; can swap to FAISS/Qdrant later.
