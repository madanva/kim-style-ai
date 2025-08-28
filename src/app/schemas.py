
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class UploadResponse(BaseModel):
    count: int

class CrawlRequest(BaseModel):
    brands: List[str]

class SearchRequest(BaseModel):
    top_k: int = 20

class ProductOut(BaseModel):
    name: str
    url: HttpUrl | str
    thumb_url: Optional[str] = None
    brand: Optional[str] = None
    score: float
