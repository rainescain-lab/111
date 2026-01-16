import csv
import os
import sys
import time
from typing import Any, Dict, List

from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

USER_DATA_DIR = os.environ.get("USER_DATA_DIR", r"C:\playwright_profiles\amazon")
KEYWORD = os.environ.get("KEYWORD", "hair loss")
MAX_PAGES = int(os.environ.get("MAX_PAGES", "5"))
OUT_CSV = os.environ.get("OUT_CSV", "amazon_search_results.csv")
HEADLESS = os.environ.get("HEADLESS", "0") == "1"
SLOW_MO_MS = int(os.environ.get("SLOW_MO_MS", "80"))
CARD_DEADLINE_SEC = float(os.environ.get("CARD_DEADLINE_SEC", "1.2"))
FLUSH_EVERY = int(os.environ.get("FLUSH_EVERY", "10"))
EXCLUDE_SPONSORED = os.environ.get("EXCLUDE_SPONSORED", "0") == "1"

DEFAULT_TIMEOUT_MS = 3000
NAV_TIMEOUT_MS = 10000


def debug(message: str) -> None:
    print(f"[DEBUG] {message}", flush=True)


def warn(message: str) -> None:
    print(f"[WARN] {message}", flush=True)


def detect_captcha(page) -> bool:
    try:
        content = page.content()
    except PlaywrightError:
        return False
    lower = content.lower()
    return any(
        token in lower
        for token in (
            "captcha",
            "robot check",
            "unusual traffic",
            "enter the characters you see below",
            "validatecaptcha",
        )
    )


def wait_for_manual_resolution() -> None:
    print(
        "[WARN] Detected captcha/robot check. Please resolve it manually in the "
        "browser, then press Enter to continue.",
        flush=True,
    )
    try:
        input()
    except EOFError:
        time.sleep(3)


def extract_card_data(handle, timeout_ms: int) -> Dict[str, Any]:
    return handle.evaluate(
        """
        (el, deadlineMs) => {
          const extract = () => {
            const pickText = (node) => node ? node.textContent.trim() : "";
            const cleanText = (value) => value.replace(/\\s+/g, " ").trim();
            const scrubAdText = (value) =>
              value
                .replace(/sponsored/gi, "")
                .replace(/you['’]re seeing this ad/gi, "")
                .replace(/leave ad feedback/gi, "")
                .replace(/learn more/gi, "")
                .replace(/why this ad\\??/gi, "")
                .replace(/report this ad\\??/gi, "")
                .replace(/shop now/gi, "")
                .replace(/details/gi, "")
                .replace(/visit the store/gi, "")
                .replace(/shop now/gi, "")
                .replace(/\\s+/g, " ")
                .trim();
            const primaryTitleNode = el.querySelector("h2 a span");
            const fallbackTitleNodes = Array.from(
              el.querySelectorAll(
                "span.a-size-base-plus.a-color-base.a-text-normal, " +
                  "span.a-size-medium.a-color-base.a-text-normal, " +
                  "[data-cy='title-recipe'] span, " +
                  "h2"
              )
            );
            const titleCandidates = [];
            if (primaryTitleNode && primaryTitleNode.textContent) {
              titleCandidates.push(primaryTitleNode.textContent);
            }
            for (const node of fallbackTitleNodes) {
              if (node && node.textContent) {
                titleCandidates.push(node.textContent);
              }
            }
            const cleanedCandidates = titleCandidates
              .map((text) => scrubAdText(cleanText(text || "")))
              .filter((text) => text.length > 0);
            const title =
              cleanedCandidates.find((text) => text.length >= 8) ||
              cleanedCandidates.sort((a, b) => b.length - a.length)[0] ||
              "";
            const linkEl =
              el.querySelector("a[href*='/dp/']") ||
              el.querySelector("a[href*='/gp/']");
            const allLinks = linkEl ? [linkEl] : Array.from(el.querySelectorAll("a[href]"));
            const hrefMatch = allLinks.find((node) => {
              const href = node.getAttribute("href") || "";
              return href.includes("/dp/") || href.includes("/gp/");
            });
            const priceEl = el.querySelector(".a-price .a-offscreen");
            const ratingEl = el.querySelector("span.a-icon-alt");
            const reviewsEl =
              el.querySelector("span.s-underline-text") ||
              el.querySelector("a[href*='customerReviews'] span") ||
              el.querySelector("span[aria-label$='ratings'], span[aria-label$='rating']");
            const asin = el.getAttribute("data-asin") || "";
            const url = hrefMatch ? hrefMatch.href : "";
            const price = pickText(priceEl);
            const rating = pickText(ratingEl);
            const reviews = pickText(reviewsEl);
            const sponsoredLabel =
              el.querySelector("[aria-label*='Sponsored'], [aria-label*='sponsored']") ||
              Array.from(el.querySelectorAll("span")).find(
                (node) => cleanText(node.textContent || "") === "Sponsored"
              );
            const is_sponsored = Boolean(sponsoredLabel);
            return { asin, title, url, price, rating, reviews, is_sponsored };
          };
          const timeout = () =>
            new Promise((resolve) =>
              setTimeout(() => resolve({ timeout: true }), deadlineMs)
            );
          return Promise.race([Promise.resolve().then(extract), timeout()]);
        }
        """,
        timeout_ms,
    )


def flush_rows(rows: List[Dict[str, Any]], writer, csv_file) -> None:
    if not rows:
        return
    writer.writerows(rows)
    csv_file.flush()
    os.fsync(csv_file.fileno())
    rows.clear()


def main() -> int:
    keyword = KEYWORD.strip()
    if not keyword:
        print("KEYWORD is empty.")
        return 1

    os.makedirs(os.path.dirname(os.path.abspath(OUT_CSV)) or ".", exist_ok=True)

    fieldnames = [
        "keyword",
        "page",
        "rank",
        "asin",
        "title",
        "price",
        "rating",
        "reviews",
        "url",
        "is_sponsored",
    ]

    total_rank = 0
    rows: List[Dict[str, Any]] = []

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=HEADLESS,
            slow_mo=SLOW_MO_MS,
        )
        context.set_default_timeout(DEFAULT_TIMEOUT_MS)
        page = context.pages[0] if context.pages else context.new_page()

        try:
            page.goto(
                "https://www.amazon.com",
                timeout=NAV_TIMEOUT_MS,
                wait_until="domcontentloaded",
            )
            if detect_captcha(page):
                wait_for_manual_resolution()

            search_box = page.locator("input#twotabsearchtextbox")
            search_box.fill(keyword, timeout=DEFAULT_TIMEOUT_MS)
            search_box.press("Enter", timeout=DEFAULT_TIMEOUT_MS)

            with open(OUT_CSV, "a", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if csv_file.tell() == 0:
                    writer.writeheader()

                for page_index in range(1, MAX_PAGES + 1):
                    page.wait_for_load_state("domcontentloaded", timeout=NAV_TIMEOUT_MS)
                    if detect_captcha(page):
                        wait_for_manual_resolution()

                    try:
                        page.wait_for_selector(
                            'div.s-main-slot div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])',
                            timeout=DEFAULT_TIMEOUT_MS,
                        )
                    except PlaywrightTimeoutError:
                        warn(f"Page {page_index} results not ready in time; continuing.")

                    current_url = page.url
                    card_locator = page.locator(
                        'div.s-main-slot div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])'
                    )
                    try:
                        card_count = card_locator.count()
                    except PlaywrightTimeoutError:
                        card_count = 0

                    debug(f"Page {page_index} URL: {current_url}")
                    debug(f"Page {page_index} cards: {card_count}")

                    try:
                        cards = card_locator.element_handles()
                    except PlaywrightError as exc:
                        debug(f"Skipping page {page_index} due to error: {exc}")
                        cards = []

                    for idx, handle in enumerate(cards, start=1):
                        deadline_ms = max(200, int(CARD_DEADLINE_SEC * 1000))
                        try:
                            data = extract_card_data(handle, timeout_ms=deadline_ms)
                        except PlaywrightTimeoutError:
                            warn(f"card {idx} timeout")
                            continue
                        except PlaywrightError as exc:
                            warn(f"card {idx} skipped: {exc}")
                            continue
                        if data.get("timeout"):
                            warn(f"card {idx} timeout")
                            continue

                        asin = (data.get("asin") or "").strip()
                        if not asin:
                            warn(f"card {idx} skipped: empty ASIN")
                            continue
                        if EXCLUDE_SPONSORED and data.get("is_sponsored"):
                            warn(f"card {idx} skipped: sponsored")
                            continue

                        url = (data.get("url") or "").strip()
                        if not url:
                            url = f"https://www.amazon.com/dp/{asin}"

                        total_rank += 1
                        rows.append(
                            {
                                "keyword": keyword,
                                "page": page_index,
                                "rank": total_rank,
                                "asin": asin,
                                "title": data.get("title", "").strip(),
                                "price": data.get("price", "").strip(),
                                "rating": data.get("rating", "").strip(),
                                "reviews": data.get("reviews", "").strip(),
                                "url": url,
                                "is_sponsored": bool(data.get("is_sponsored")),
                            }
                        )

                        if len(rows) >= FLUSH_EVERY:
                            flush_rows(rows, writer, csv_file)

                    flush_rows(rows, writer, csv_file)

                    next_button = page.locator("a.s-pagination-next:not(.s-pagination-disabled)")
                    try:
                        has_next = next_button.count() > 0
                    except PlaywrightTimeoutError:
                        has_next = False

                    if not has_next:
                        debug("No Next button found; stopping pagination.")
                        break

                    try:
                        next_button.first.click(timeout=DEFAULT_TIMEOUT_MS)
                    except PlaywrightTimeoutError:
                        debug("Next button click timed out; stopping pagination.")
                        break
                    except PlaywrightError as exc:
                        debug(f"Next button click failed: {exc}")
                        break

        except KeyboardInterrupt:
            debug("Interrupted by user.")
        finally:
            try:
                context.close()
            except PlaywrightError:
                pass

    debug(f"Saved {total_rank} rows -> {OUT_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
