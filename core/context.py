from __future__ import annotations

import re
from pathlib import Path

from config import CATEGORY_KEYWORDS, MIN_CATEGORY_CHARS, PAGES_DIR


def load_pages_file(prop_id: str) -> str | None:
    path = Path(PAGES_DIR) / f"{prop_id}-pages.txt"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def filter_by_keywords(text: str, keywords: list[str]) -> str:
    if not text.strip():
        return ""
    pattern = re.compile("|".join(re.escape(keyword) for keyword in keywords), re.IGNORECASE)
    blocks = re.split(r"\n\s*\n", text)
    matched = [block.strip() for block in blocks if pattern.search(block)]
    return "\n\n".join(block for block in matched if block)


def prepare_context(prop_id: str, category: str) -> dict:
    full_text = load_pages_file(prop_id)
    if full_text is None:
        return {
            "full_text": None,
            "filtered_text": "",
            "use_search": True,
            "source": "search_only",
        }

    keywords = CATEGORY_KEYWORDS[category]
    filtered_text = filter_by_keywords(full_text, keywords)
    if len(filtered_text) >= MIN_CATEGORY_CHARS:
        return {
            "full_text": full_text,
            "filtered_text": filtered_text,
            "use_search": False,
            "source": "pages",
        }

    keyword_pattern = re.compile("|".join(re.escape(keyword) for keyword in keywords), re.IGNORECASE)
    has_any_keyword = bool(keyword_pattern.search(full_text))
    return {
        "full_text": full_text,
        "filtered_text": full_text if has_any_keyword else filtered_text,
        "use_search": not has_any_keyword,
        "source": "pages",
    }
