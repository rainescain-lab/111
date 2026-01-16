from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QuerySlice:
    slice_id: str
    keyword: str
    browse_node: Optional[str]
    price_min: int
    price_max: int
    brand: Optional[str]
    sort: Optional[str]
    page_limit: int
    status: str


@dataclass(frozen=True)
class SearchPageTask:
    task_id: str
    slice_id: str
    page_no: int
    status: str
    attempts: int
    last_error: Optional[str]


@dataclass(frozen=True)
class AsinTask:
    task_id: str
    asin: str
    depth: int
    status: str
    attempts: int
    last_error: Optional[str]


@dataclass(frozen=True)
class Product:
    asin: str
    title: str
    price_text: str
    rating_text: str
    reviews_text: str
    canonical_url: str
    first_seen_at: str
    last_seen_at: str
    sources: str
