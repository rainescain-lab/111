# Amazon Search Coverage Scraper (Playwright + SQLite)

This project provides a **stable, resumable** Amazon scraping framework for Windows using **Playwright (sync API)** and **SQLite**. It focuses on **coverage over depth** by **slicing the search space** and optionally **graph-expanding ASINs**, while avoiding any anti-bot bypasses.

> ✅ No captcha circumvention. If a challenge is detected, the script pauses for manual resolution.

---

## ✅ Features

- **Persistent login** via `launch_persistent_context`
- **Search slicing** (price buckets, optional browse node/brand)
- **SQLite state** for resumable crawling + global dedupe
- **Graph expansion** via ASIN relationships (optional)
- **Batch extraction** via single `page.evaluate`
- **Structured logging** with task context
- **CSV export**
- **Tests** for URL/ASIN parsing, dedupe, slicing

---

## 📦 Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install playwright
playwright install chromium
```

---

## ▶️ Usage

### Run the crawler

```bash
python -m amazon_scraper.cli run --keyword "hair loss" --page-limit 3
```

### Export CSV

```bash
python -m amazon_scraper.cli export --out-csv amazon_results.csv
```

### Stats

```bash
python -m amazon_scraper.cli stats
```

---

## ⚙️ Environment Variables

All CLI args can be overridden via env vars:

| Variable | Description | Default |
|---|---|---|
| `USER_DATA_DIR` | Persistent Playwright profile dir | `C:\playwright_profiles\amazon` |
| `KEYWORD` | Single keyword if not using file | `hair loss` |
| `KEYWORDS_FILE` | CSV file with keywords | *(optional)* |
| `OUT_DB` | SQLite DB path | `amazon_scraper.db` |
| `OUT_CSV` | CSV export path | `amazon_export.csv` |
| `PAGE_LIMIT` | Max pages per slice | `5` |
| `PRICE_MIN` / `PRICE_MAX` | Price bounds | `0` / `200` |
| `MIN_PRICE_BUCKET` | Minimum bucket width | `10` |
| `ENABLE_GRAPH_EXPANSION` | Expand ASIN graph | `0` |
| `GRAPH_DEPTH` | BFS depth | `2` |
| `GRAPH_BUDGET` | Max ASIN expansions | `200` |
| `HEADLESS` | Headless mode | `0` |
| `SLOW_MO_MS` | Slow motion delay | `80` |
| `NAV_TIMEOUT_MS` | Navigation timeout | `15000` |
| `ACTION_TIMEOUT_MS` | Action timeout | `4000` |
| `EXCLUDE_SPONSORED` | Skip sponsored cards | `0` |

---

## ❓ FAQ

### Captcha / Robot Check
The crawler **never bypasses** captcha. If detected, it will pause and prompt:

```
[WARN] Captcha detected. Please solve in the browser, then press Enter.
```

### Login / Locale
Make sure your persistent profile (`USER_DATA_DIR`) is already logged in and set to your desired **region/language**.

### Resume after interruption
SQLite tracks all slices/pages/tasks. Simply rerun `run`.

---

## 📁 Project Structure

See `amazon_scraper_project/` for the full layout. The main entrypoint is:

```
python -m amazon_scraper.cli run
```

