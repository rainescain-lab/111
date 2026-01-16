import json
import os
import tempfile

from amazon_scraper.db import Database


def test_product_dedupe_updates_sources() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = Database(db_path)
        db.upsert_product(
            {
                "asin": "B000000001",
                "title": "Title",
                "price_text": "$9.99",
                "rating_text": "4.5",
                "reviews_text": "10",
                "canonical_url": "https://www.amazon.com/dp/B000000001",
                "first_seen_at": "2024-01-01T00:00:00",
                "sources": [{"slice_id": "s1"}],
            }
        )
        db.upsert_product(
            {
                "asin": "B000000001",
                "title": "Title 2",
                "price_text": "$9.99",
                "rating_text": "4.6",
                "reviews_text": "11",
                "canonical_url": "https://www.amazon.com/dp/B000000001",
                "first_seen_at": "2024-01-01T00:00:00",
                "sources": [{"slice_id": "s2"}],
            }
        )
        rows = db.fetch_products()
        assert len(rows) == 1
        sources = json.loads(rows[0]["sources"])
        assert len(sources) == 2
