from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Settings:
    user_data_dir: str
    keyword: str
    keywords_file: str | None
    out_db: str
    out_csv: str
    page_limit: int
    price_min: int
    price_max: int
    min_price_bucket: int
    enable_graph_expansion: bool
    graph_depth: int
    graph_budget: int
    headless: bool
    slow_mo_ms: int
    nav_timeout_ms: int
    action_timeout_ms: int
    exclude_sponsored: bool


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name, str(default))
    return int(value)


def _env_bool(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default) == "1"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Amazon search coverage scraper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run scraper")
    run_parser.add_argument("--keyword", default=os.environ.get("KEYWORD", "hair loss"))
    run_parser.add_argument("--keywords-file", default=os.environ.get("KEYWORDS_FILE"))
    run_parser.add_argument("--page-limit", type=int, default=_env_int("PAGE_LIMIT", 5))
    run_parser.add_argument("--price-min", type=int, default=_env_int("PRICE_MIN", 0))
    run_parser.add_argument("--price-max", type=int, default=_env_int("PRICE_MAX", 200))
    run_parser.add_argument("--min-price-bucket", type=int, default=_env_int("MIN_PRICE_BUCKET", 10))
    run_parser.add_argument("--enable-graph-expansion", action="store_true", default=_env_bool("ENABLE_GRAPH_EXPANSION"))
    run_parser.add_argument("--graph-depth", type=int, default=_env_int("GRAPH_DEPTH", 2))
    run_parser.add_argument("--graph-budget", type=int, default=_env_int("GRAPH_BUDGET", 200))
    run_parser.add_argument("--exclude-sponsored", action="store_true", default=_env_bool("EXCLUDE_SPONSORED"))

    export_parser = subparsers.add_parser("export", help="Export CSV")
    export_parser.add_argument("--out-csv", default=os.environ.get("OUT_CSV", "amazon_export.csv"))

    subparsers.add_parser("stats", help="Print stats")

    parser.add_argument("--user-data-dir", default=os.environ.get("USER_DATA_DIR", r"C:\playwright_profiles\amazon"))
    parser.add_argument("--out-db", default=os.environ.get("OUT_DB", "amazon_scraper.db"))
    parser.add_argument("--out-csv", default=os.environ.get("OUT_CSV", "amazon_export.csv"))
    parser.add_argument("--headless", action="store_true", default=_env_bool("HEADLESS"))
    parser.add_argument("--slow-mo-ms", type=int, default=_env_int("SLOW_MO_MS", 80))
    parser.add_argument("--nav-timeout-ms", type=int, default=_env_int("NAV_TIMEOUT_MS", 15000))
    parser.add_argument("--action-timeout-ms", type=int, default=_env_int("ACTION_TIMEOUT_MS", 4000))

    return parser


def parse_args(argv: List[str] | None = None) -> tuple[str, Settings]:
    parser = build_parser()
    args = parser.parse_args(argv)

    settings = Settings(
        user_data_dir=args.user_data_dir,
        keyword=args.keyword if hasattr(args, "keyword") else os.environ.get("KEYWORD", "hair loss"),
        keywords_file=args.keywords_file if hasattr(args, "keywords_file") else os.environ.get("KEYWORDS_FILE"),
        out_db=args.out_db,
        out_csv=args.out_csv,
        page_limit=args.page_limit if hasattr(args, "page_limit") else _env_int("PAGE_LIMIT", 5),
        price_min=args.price_min if hasattr(args, "price_min") else _env_int("PRICE_MIN", 0),
        price_max=args.price_max if hasattr(args, "price_max") else _env_int("PRICE_MAX", 200),
        min_price_bucket=args.min_price_bucket if hasattr(args, "min_price_bucket") else _env_int("MIN_PRICE_BUCKET", 10),
        enable_graph_expansion=args.enable_graph_expansion if hasattr(args, "enable_graph_expansion") else _env_bool("ENABLE_GRAPH_EXPANSION"),
        graph_depth=args.graph_depth if hasattr(args, "graph_depth") else _env_int("GRAPH_DEPTH", 2),
        graph_budget=args.graph_budget if hasattr(args, "graph_budget") else _env_int("GRAPH_BUDGET", 200),
        headless=args.headless,
        slow_mo_ms=args.slow_mo_ms,
        nav_timeout_ms=args.nav_timeout_ms,
        action_timeout_ms=args.action_timeout_ms,
        exclude_sponsored=args.exclude_sponsored if hasattr(args, "exclude_sponsored") else _env_bool("EXCLUDE_SPONSORED"),
    )

    return args.command, settings
