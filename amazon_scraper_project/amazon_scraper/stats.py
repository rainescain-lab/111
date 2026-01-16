from __future__ import annotations

from .db import Database


def print_stats(db_path: str) -> None:
    db = Database(db_path)
    print(f"query_slices: {db.count_rows('query_slices')}")
    print(f"search_pages: {db.count_rows('search_pages')}")
    print(f"products: {db.count_rows('products')}")
    print(f"asin_tasks: {db.count_rows('asin_tasks')}")
    print(f"asin_edges: {db.count_rows('asin_edges')}")
