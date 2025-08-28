
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import zipfile, shutil, os
from typing import List
from .db import SessionLocal, init_db, engine
from .models import Base, ReferenceImage, Product
from .embeddings import embed_image
from sqlalchemy import select, text
from pydantic import BaseModel
from .schemas import UploadResponse, CrawlRequest, SearchRequest, ProductOut
import dramatiq
from dramatiq.brokers.redis import RedisBroker
import json

# Dramatiq setup
import os as _os
broker = RedisBroker(url=_os.getenv("REDIS_URL", "redis://localhost:6379/0"))
dramatiq.set_broker(broker)

app = FastAPI(title="Kim Style AI — MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables + extension
Base.metadata.create_all(bind=engine)
init_db()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

@app.post("/upload-references", response_model=UploadResponse)
async def upload_references(files: List[UploadFile] = File(...)):
    saved = 0
    with SessionLocal() as db:
        for f in files:
            dst = UPLOAD_DIR / f.filename
            with dst.open("wb") as out:
                out.write(await f.read())
            # Skip ZIP handling for brevity; could expand here
            vec = embed_image(str(dst))
            db.add(ReferenceImage(path=str(dst), embed=vec))
            saved += 1
        db.commit()
    return UploadResponse(count=saved)

@app.post("/crawl")
async def crawl(req: CrawlRequest):
    # Enqueue async crawl per brand
    from src.worker.tasks import crawl_brand
    for brand in req.brands:
        crawl_brand.send(brand)
    return {"queued": req.brands}

@app.post("/search", response_model=List[ProductOut])
async def search(req: SearchRequest):
    # Compute centroid of reference vectors, then ANN over products
    from sqlalchemy import func
    with SessionLocal() as db:
        refs = db.execute(select(ReferenceImage.embed)).scalars().all()
        if not refs:
            return []
        import numpy as np
        centroid = np.array(refs).mean(axis=0)
        # cosine similarity with pgvector: 1 - (embed <=> centroid)
        rows = db.execute(text("""
            SELECT name, url, thumb_url, brand,
                   1 - (embed <=> :q) AS score
            FROM products
            WHERE embed IS NOT NULL
            ORDER BY embed <=> :q
            LIMIT :k
        """), {"q": list(centroid), "k": req.top_k}).all()
        return [ProductOut(name=r[0], url=r[1], thumb_url=r[2], brand=r[3], score=float(r[4])) for r in rows]

@app.get("/healthz")
def healthz():
    return {"ok": True}
