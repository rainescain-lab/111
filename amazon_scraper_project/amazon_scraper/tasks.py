from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from playwright.sync_api import Error as PlaywrightError, Page

from .browser import BrowserSession, detect_captcha, wait_for_manual_resolution
from .config import Settings
from .db import Database, utc_now
from .extractor import extract_cards
from .slicer import PriceRange, build_initial_ranges, should_split, split_price_range


def build_logger() -> logging.Logger:
    logger = logging.getLogger("amazon_scraper")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s [task=%(task_id)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def make_task_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def run_with_retry(
    logger: logging.Logger,
    task_id: str,
    attempts: int,
    max_attempts: int,
    action,
) -> None:
    try:
        action()
    except Exception as exc:
        attempts += 1
        logger.warning(
            "Attempt %s/%s failed: %s", attempts, max_attempts, exc, extra={"task_id": task_id}
        )
        if attempts >= max_attempts:
            raise
        time.sleep(min(2 ** attempts, 10))


def normalize_url(asin: str, url: str) -> str:
    if not url:
        return f"https://www.amazon.com/dp/{asin}"
    return url


def load_keywords(settings: Settings) -> List[str]:
    if settings.keywords_file:
        with open(settings.keywords_file, "r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle.readlines() if line.strip()]
        return lines
    return [settings.keyword]


def slice_id_for(keyword: str, price_range: PriceRange, browse_node: Optional[str]) -> str:
    node = browse_node or "none"
    return f"{keyword}-{node}-{price_range.min_price}-{price_range.max_price}"


def seed_slices(db: Database, settings: Settings, logger: logging.Logger) -> None:
    for keyword in load_keywords(settings):
        for price_range in build_initial_ranges(settings.price_min, settings.price_max):
            slice_id = slice_id_for(keyword, price_range, None)
            db.upsert_slice(
                QuerySlice(
                    slice_id=slice_id,
                    keyword=keyword,
                    browse_node=None,
                    price_min=price_range.min_price,
                    price_max=price_range.max_price,
                    brand=None,
                    sort=None,
                    page_limit=settings.page_limit,
                    status="pending",
                )
            )
            db.enqueue_search_page(make_task_id("page"), slice_id, 1)
            logger.info("Seeded slice %s", slice_id, extra={"task_id": "seed"})


def ensure_logged_in(page: Page, settings: Settings) -> None:
    page.goto("https://www.amazon.com", timeout=settings.nav_timeout_ms, wait_until="domcontentloaded")
    if detect_captcha(page):
        wait_for_manual_resolution()


def search_page_url(keyword: str, page_no: int) -> str:
    if page_no <= 1:
        return f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    return f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&page={page_no}"


def execute_search_page(
    page: Page,
    settings: Settings,
    slice_id: str,
    keyword: str,
    page_no: int,
    logger: logging.Logger,
) -> tuple[List[Dict[str, str]], bool]:
    page.goto(search_page_url(keyword, page_no), timeout=settings.nav_timeout_ms, wait_until="domcontentloaded")
    if detect_captcha(page):
        wait_for_manual_resolution()
    page.wait_for_timeout(500)
    cards = extract_cards(page)
    logger.info(
        "Fetched page %s with %s cards",
        page_no,
        len(cards),
        extra={"task_id": f"{slice_id}:{page_no}"},
    )

    normalized_cards = []
    for card in cards:
        asin = (card.get("asin") or "").strip()
        if not asin:
            continue
        if settings.exclude_sponsored and card.get("is_sponsored"):
            continue
        url = normalize_url(asin, (card.get("url") or "").strip())
        normalized_cards.append(
            {
                "asin": asin,
                "title": (card.get("title") or "").strip(),
                "price_text": (card.get("price_text") or "").strip(),
                "rating_text": (card.get("rating_text") or "").strip(),
                "reviews_text": (card.get("reviews_text") or "").strip(),
                "canonical_url": url,
                "rank_in_page": card.get("rank_in_page", 0),
                "is_sponsored": bool(card.get("is_sponsored")),
            }
        )

    has_next = bool(page.query_selector("a.s-pagination-next:not(.s-pagination-disabled)"))
    return normalized_cards, has_next


def execute_slice(
    session: BrowserSession,
    db: Database,
    settings: Settings,
    slice_id: str,
    keyword: str,
    price_range: PriceRange,
    logger: logging.Logger,
) -> None:
    def handler(page: Page) -> None:
        ensure_logged_in(page, settings)
        too_large = False
        for page_no in range(1, settings.page_limit + 1):
            cards, has_next = execute_search_page(page, settings, slice_id, keyword, page_no, logger)
            for card in cards:
                db.upsert_product(
                    {
                        "asin": card["asin"],
                        "title": card["title"],
                        "price_text": card["price_text"],
                        "rating_text": card["rating_text"],
                        "reviews_text": card["reviews_text"],
                        "canonical_url": card["canonical_url"],
                        "first_seen_at": utc_now(),
                        "sources": [
                            {
                                "slice_id": slice_id,
                                "page_no": page_no,
                                "rank_in_page": card.get("rank_in_page", 0),
                                "keyword": keyword,
                                "seen_at": utc_now(),
                                "is_sponsored": card.get("is_sponsored", False),
                            }
                        ],
                    }
                )
            if not has_next:
                break
            if page_no == settings.page_limit and has_next:
                too_large = True
        if too_large and should_split(price_range, settings.min_price_bucket):
            left, right = split_price_range(price_range)
            for child in (left, right):
                child_slice_id = slice_id_for(keyword, child, None)
                db.upsert_slice(
                    QuerySlice(
                        slice_id=child_slice_id,
                        keyword=keyword,
                        browse_node=None,
                        price_min=child.min_price,
                        price_max=child.max_price,
                        brand=None,
                        sort=None,
                        page_limit=settings.page_limit,
                        status="pending",
                    )
                )
                db.enqueue_search_page(make_task_id("page"), child_slice_id, 1)
                logger.info("Split slice -> %s", child_slice_id, extra={"task_id": slice_id})

    session.run(handler)


def run_tasks(settings: Settings) -> None:
    logger = build_logger()
    db = Database(settings.out_db)
    seed_slices(db, settings, logger)
    session = BrowserSession(
        user_data_dir=settings.user_data_dir,
        headless=settings.headless,
        slow_mo_ms=settings.slow_mo_ms,
        nav_timeout_ms=settings.nav_timeout_ms,
        action_timeout_ms=settings.action_timeout_ms,
    )

    while True:
        row = db.fetch_next_search_page()
        if not row:
            break
        task_id = row["task_id"]
        slice_id = row["slice_id"]
        page_no = row["page_no"]
        attempts = row["attempts"]
        logger.info("Processing page task", extra={"task_id": task_id})

        def action() -> None:
            execute_slice(
                session=session,
                db=db,
                settings=settings,
                slice_id=slice_id,
                keyword=slice_id.split("-")[0],
                price_range=PriceRange(settings.price_min, settings.price_max),
                logger=logger,
            )

        try:
            run_with_retry(logger, task_id, attempts, 3, action)
            db.update_search_page(task_id, "done", attempts + 1, None)
        except Exception as exc:
            db.update_search_page(task_id, "failed", attempts + 1, str(exc))

        if settings.enable_graph_expansion:
            run_asin_expansion(session, db, settings, logger)


def run_asin_expansion(session: BrowserSession, db: Database, settings: Settings, logger: logging.Logger) -> None:
    budget = settings.graph_budget
    while budget > 0:
        task = db.fetch_next_asin_task()
        if not task:
            break
        task_id = task["task_id"]
        asin = task["asin"]
        depth = task["depth"]
        attempts = task["attempts"]
        logger.info("Processing ASIN task", extra={"task_id": task_id})

        if depth >= settings.graph_depth:
            db.update_asin_task(task_id, "done", attempts, None)
            continue

        def action() -> None:
            def handler(page: Page) -> None:
                page.goto(
                    f"https://www.amazon.com/dp/{asin}",
                    timeout=settings.nav_timeout_ms,
                    wait_until="domcontentloaded",
                )
                if detect_captcha(page):
                    wait_for_manual_resolution()
                related = page.evaluate(
                    """
                    () => {
                      const links = Array.from(document.querySelectorAll("a[href*='/dp/']"));
                      const asins = new Set();
                      for (const link of links) {
                        const match = link.href.match(/\\/dp\\/([A-Z0-9]{10})/i);
                        if (match) {
                          asins.add(match[1].toUpperCase());
                        }
                      }
                      return Array.from(asins).slice(0, 20);
                    }
                    """
                )
                for related_asin in related:
                    db.insert_edge(asin, related_asin, "related")
                    db.enqueue_asin_task(make_task_id("asin"), related_asin, depth + 1)

            session.run(handler)

        try:
            run_with_retry(logger, task_id, attempts, 3, action)
            db.update_asin_task(task_id, "done", attempts + 1, None)
            budget -= 1
        except Exception as exc:
            db.update_asin_task(task_id, "failed", attempts + 1, str(exc))
            budget -= 1


# Local import to avoid circular dependency in the seed function.
from .models import QuerySlice  # noqa: E402
