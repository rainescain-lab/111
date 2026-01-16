from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Iterable, Iterator, Optional

from .models import QuerySlice


def utc_now() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self._ensure_schema()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _ensure_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                create table if not exists query_slices (
                    slice_id text primary key,
                    keyword text not null,
                    browse_node text,
                    price_min integer,
                    price_max integer,
                    brand text,
                    sort text,
                    page_limit integer,
                    status text,
                    created_at text,
                    updated_at text
                );
                create table if not exists search_pages (
                    task_id text primary key,
                    slice_id text,
                    page_no integer,
                    status text,
                    attempts integer,
                    last_error text
                );
                create table if not exists products (
                    asin text primary key,
                    title text,
                    price_text text,
                    rating_text text,
                    reviews_text text,
                    canonical_url text,
                    first_seen_at text,
                    last_seen_at text,
                    sources text
                );
                create table if not exists asin_edges (
                    from_asin text,
                    to_asin text,
                    edge_type text,
                    seen_at text
                );
                create table if not exists asin_tasks (
                    task_id text primary key,
                    asin text,
                    depth integer,
                    status text,
                    attempts integer,
                    last_error text
                );
                """
            )

    def upsert_slice(self, slice_row: QuerySlice) -> None:
        with self.connect() as conn:
            now = utc_now()
            conn.execute(
                """
                insert into query_slices (
                    slice_id, keyword, browse_node, price_min, price_max, brand, sort,
                    page_limit, status, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(slice_id) do update set
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    slice_row.slice_id,
                    slice_row.keyword,
                    slice_row.browse_node,
                    slice_row.price_min,
                    slice_row.price_max,
                    slice_row.brand,
                    slice_row.sort,
                    slice_row.page_limit,
                    slice_row.status,
                    now,
                    now,
                ),
            )

    def enqueue_search_page(self, task_id: str, slice_id: str, page_no: int) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                insert or ignore into search_pages (
                    task_id, slice_id, page_no, status, attempts, last_error
                ) values (?, ?, ?, 'pending', 0, null)
                """,
                (task_id, slice_id, page_no),
            )

    def fetch_next_search_page(self) -> Optional[sqlite3.Row]:
        with self.connect() as conn:
            row = conn.execute(
                """
                select * from search_pages
                where status in ('pending', 'retry')
                order by rowid asc
                limit 1
                """
            ).fetchone()
            return row

    def update_search_page(self, task_id: str, status: str, attempts: int, last_error: Optional[str]) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                update search_pages
                set status = ?, attempts = ?, last_error = ?
                where task_id = ?
                """,
                (status, attempts, last_error, task_id),
            )

    def upsert_product(self, product: Dict[str, Any]) -> None:
        with self.connect() as conn:
            existing = conn.execute(
                "select sources from products where asin = ?", (product["asin"],)
            ).fetchone()
            sources = product.get("sources", [])
            if existing:
                try:
                    existing_sources = json.loads(existing["sources"])
                except json.JSONDecodeError:
                    existing_sources = []
                sources = existing_sources + sources
            now = utc_now()
            conn.execute(
                """
                insert into products (
                    asin, title, price_text, rating_text, reviews_text,
                    canonical_url, first_seen_at, last_seen_at, sources
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(asin) do update set
                    title = excluded.title,
                    price_text = excluded.price_text,
                    rating_text = excluded.rating_text,
                    reviews_text = excluded.reviews_text,
                    canonical_url = excluded.canonical_url,
                    last_seen_at = excluded.last_seen_at,
                    sources = excluded.sources
                """,
                (
                    product["asin"],
                    product.get("title", ""),
                    product.get("price_text", ""),
                    product.get("rating_text", ""),
                    product.get("reviews_text", ""),
                    product.get("canonical_url", ""),
                    product.get("first_seen_at", now),
                    now,
                    json.dumps(sources, ensure_ascii=False),
                ),
            )

    def insert_edge(self, from_asin: str, to_asin: str, edge_type: str) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                insert into asin_edges (from_asin, to_asin, edge_type, seen_at)
                values (?, ?, ?, ?)
                """,
                (from_asin, to_asin, edge_type, utc_now()),
            )

    def enqueue_asin_task(self, task_id: str, asin: str, depth: int) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                insert or ignore into asin_tasks (
                    task_id, asin, depth, status, attempts, last_error
                ) values (?, ?, ?, 'pending', 0, null)
                """,
                (task_id, asin, depth),
            )

    def fetch_next_asin_task(self) -> Optional[sqlite3.Row]:
        with self.connect() as conn:
            return conn.execute(
                """
                select * from asin_tasks
                where status in ('pending', 'retry')
                order by rowid asc
                limit 1
                """
            ).fetchone()

    def update_asin_task(self, task_id: str, status: str, attempts: int, last_error: Optional[str]) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                update asin_tasks
                set status = ?, attempts = ?, last_error = ?
                where task_id = ?
                """,
                (status, attempts, last_error, task_id),
            )

    def count_rows(self, table: str) -> int:
        with self.connect() as conn:
            row = conn.execute(f"select count(*) as count from {table}").fetchone()
            return int(row["count"])

    def fetch_products(self) -> Iterable[sqlite3.Row]:
        with self.connect() as conn:
            return conn.execute("select * from products").fetchall()

    def fetch_search_pages(self) -> Iterable[sqlite3.Row]:
        with self.connect() as conn:
            return conn.execute("select * from search_pages").fetchall()
