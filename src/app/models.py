
from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, JSON, Text, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from .db import Base

EMBED_DIM = 768  # ViT-L/14

class ReferenceImage(Base):
    __tablename__ = "reference_images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String(512))
    embed: Mapped[list[float]] = mapped_column(Vector(EMBED_DIM))

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(Text, unique=True)
    thumb_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    embed: Mapped[list[float] | None] = mapped_column(Vector(EMBED_DIM), nullable=True)

Index("ix_products_embed_hnsw", Product.embed, postgresql_using="hnsw")
