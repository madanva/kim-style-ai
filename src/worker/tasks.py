
import dramatiq
from dramatiq.middleware import AgeLimit, TimeLimit, Retries
from dramatiq.brokers.redis import RedisBroker
import os
from sqlalchemy import select
from src.app.db import SessionLocal
from src.app.models import Product
from src.crawler.base import fetch_products_for_brand

broker = RedisBroker(url=os.getenv("REDIS_URL", "redis://localhost:6379/0"))
dramatiq.set_broker(broker)

@dramatiq.actor(max_retries=3, time_limit=600_000)  # 10m
def crawl_brand(brand: str):
    items = fetch_products_for_brand(brand)
    if not items:
        return
    with SessionLocal() as db:
        for it in items:
            # upsert by URL
            exists = db.query(Product).filter_by(url=it["url"]).first()
            if exists:
                exists.name = it["name"]
                exists.thumb_url = it.get("thumb_url")
                exists.image_url = it.get("image_url")
            else:
                db.add(Product(
                    brand=brand,
                    name=it["name"],
                    url=it["url"],
                    thumb_url=it.get("thumb_url"),
                    image_url=it.get("image_url"),
                ))
        db.commit()
