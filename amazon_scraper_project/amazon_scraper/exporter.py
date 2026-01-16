from __future__ import annotations

import csv
import json
from typing import Any, Dict

from .db import Database


def export_csv(db_path: str, out_csv: str) -> None:
    db = Database(db_path)
    rows = db.fetch_products()
    fieldnames = [
        "keyword",
        "slice_id",
        "page",
        "rank_in_slice",
        "asin",
        "title",
        "price",
        "rating",
        "reviews",
        "url",
        "is_sponsored",
        "first_seen_at",
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            sources = []
            try:
                sources = json.loads(row["sources"] or "[]")
            except json.JSONDecodeError:
                sources = []
            if not sources:
                sources = [{}]
            for source in sources:
                writer.writerow(
                    {
                        "keyword": source.get("keyword", ""),
                        "slice_id": source.get("slice_id", ""),
                        "page": source.get("page_no", ""),
                        "rank_in_slice": source.get("rank_in_page", ""),
                        "asin": row["asin"],
                        "title": row["title"],
                        "price": row["price_text"],
                        "rating": row["rating_text"],
                        "reviews": row["reviews_text"],
                        "url": row["canonical_url"],
                        "is_sponsored": source.get("is_sponsored", False),
                        "first_seen_at": row["first_seen_at"],
                    }
                )
