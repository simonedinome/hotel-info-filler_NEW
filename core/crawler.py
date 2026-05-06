from __future__ import annotations

import sys
import time
from pathlib import Path

from config import FIRECRAWL_API_KEY, FIRECRAWL_MAX_DEPTH, FIRECRAWL_PAGE_LIMIT, PAGES_DIR, REQUEST_DELAY

_FIRECRAWL_CLIENT = None


def get_firecrawl_client():
    global _FIRECRAWL_CLIENT
    if _FIRECRAWL_CLIENT is None:
        from firecrawl import FirecrawlApp
        if not FIRECRAWL_API_KEY:
            raise RuntimeError("FIRECRAWL_API_KEY is not set")
        _FIRECRAWL_CLIENT = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    return _FIRECRAWL_CLIENT


def _extract_pages(result) -> list[tuple[str, str]]:
    """Return (url, markdown) pairs from a firecrawl crawl response."""
    if isinstance(result, dict):
        raw_pages = result.get("data", [])
    else:
        raw_pages = getattr(result, "data", None) or []

    pages = []
    for page in raw_pages:
        if isinstance(page, dict):
            content = page.get("markdown", "") or ""
            url = page.get("metadata", {}).get("sourceURL", "") or page.get("url", "") or ""
        else:
            content = getattr(page, "markdown", "") or ""
            meta = getattr(page, "metadata", None)
            if isinstance(meta, dict):
                url = meta.get("sourceURL", "") or ""
            else:
                url = getattr(meta, "sourceURL", "") if meta else ""
        if content.strip():
            pages.append((url, content.strip()))
    return pages


def crawl_hotel(hotel: dict, depth: int = FIRECRAWL_MAX_DEPTH, page_limit: int = FIRECRAWL_PAGE_LIMIT) -> str | None:
    """Crawl a hotel website and save content to pages/{prop_id}-pages.txt.

    Returns the output path on success, None if the website is missing or crawl fails.
    """
    prop_id = str(hotel["Property ID"])
    website = hotel.get("Sito Web", "").strip()
    if not website:
        sys.stdout.write(f"[{prop_id}] Skipping — no website configured\n")
        return None

    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    app = get_firecrawl_client()
    sys.stdout.write(f"[{prop_id}] Crawling {website}  (depth={depth}, limit={page_limit}) ...\n")
    t0 = time.monotonic()

    try:
        result = app.crawl_url(
            website,
            params={
                "maxDepth": depth,
                "limit": page_limit,
                "scrapeOptions": {"formats": ["markdown"]},
            },
        )
    except Exception as exc:
        sys.stdout.write(f"[{prop_id}] ERROR during crawl: {exc}\n")
        return None

    pages = _extract_pages(result)
    elapsed = time.monotonic() - t0

    if not pages:
        sys.stdout.write(f"[{prop_id}] No content extracted ({elapsed:.1f}s)\n")
        return None

    out_dir = Path(PAGES_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{prop_id}-pages.txt"
    out_path.write_text(
        "\n\n".join(f"=== PAGE: {url} ===\n\n{content}" for url, content in pages),
        encoding="utf-8",
    )
    sys.stdout.write(f"[{prop_id}] Saved {len(pages)} pages → {out_path}  ({elapsed:.1f}s)\n")
    return str(out_path)


def crawl_all_hotels(
    hotels: list[dict],
    depth: int = FIRECRAWL_MAX_DEPTH,
    page_limit: int = FIRECRAWL_PAGE_LIMIT,
) -> dict[str, str]:
    """Crawl all hotels that have a website URL.

    Returns a dict of {prop_id: output_path} for every successful crawl.
    """
    with_website = [h for h in hotels if h.get("Sito Web", "").strip()]
    total = len(with_website)
    results: dict[str, str] = {}

    for index, hotel in enumerate(with_website, start=1):
        prop_id = str(hotel["Property ID"])
        sys.stdout.write(f"[{index}/{total}] {hotel.get('Nome account', prop_id)}\n")
        path = crawl_hotel(hotel, depth=depth, page_limit=page_limit)
        if path:
            results[prop_id] = path
        if index < total:
            time.sleep(REQUEST_DELAY)

    sys.stdout.write(f"\nDone — crawled {len(results)}/{total} hotels successfully\n")
    return results
