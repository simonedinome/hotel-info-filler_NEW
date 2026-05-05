import os
import re
from google import genai
from google.genai import types

from config import GOOGLE_API_KEY, MODEL, PAGES_DIR, MIN_PAGES_CHARS, SYSTEM_PROMPT, CSV_COLUMNS

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client


def load_pages_file(prop_id: str) -> str | None:
    path = os.path.join(PAGES_DIR, f"{prop_id}-pages.txt")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_prompt(hotel: dict, pages_text: str | None) -> str:
    prop_id = hotel["Property ID"]
    name = hotel["Nome account"]
    website = hotel.get("Sito Web", "")
    url = ("https://" + website) if website and not website.startswith("http") else website

    lines = [
        f"Property ID: {prop_id}",
        f"Hotel Name: {name}",
    ]
    if url:
        lines.append(f"Website: {url}")

    if pages_text:
        lines += [
            "",
            "The following is the full text content extracted from this hotel's website pages.",
            "Use this as your primary source. Extract all onsite dining venues from this content.",
            "",
            "--- WEBSITE CONTENT START ---",
            pages_text.strip(),
            "--- WEBSITE CONTENT END ---",
        ]
        if url:
            lines += [
                "",
                "If the above content is insufficient for any field, you may search the web for additional information about this specific hotel's restaurants.",
            ]
    else:
        lines += [
            "",
            "No pre-scraped content is available for this hotel.",
            f"Search the web for dining information on the hotel website: {url}",
            "Focus on restaurant and bar pages. Extract all onsite dining venues.",
        ]

    lines += [
        "",
        "Follow the exact output format specified in your instructions.",
    ]

    return "\n".join(lines)


def call_gemini(hotel: dict, pages_text: str | None) -> str:
    client = get_client()
    prompt = build_prompt(hotel, pages_text)

    use_search = pages_text is None or len(pages_text) < MIN_PAGES_CHARS

    config_kwargs = {
        "system_instruction": SYSTEM_PROMPT,
        "max_output_tokens": 8192,
        "temperature": 0.1,
    }

    if use_search:
        config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    return response.text


FIELD_KEYS = [
    "Restaurant Sequence",
    "Restaurant Name",
    "Restaurant Type",
    "Phone number",
    "Hours Of Operation",
    "Cuisine Type",
    "Dietary Menu Options",
    "Meals Served",
    "Restaurant description",
    "Book a table",
    "View menu",
    "Visit Website",
    "Dining Page Headline",
    "Dining Page Description",
    "Experience Page Dining Headline",
    "Experience Page Dining Description",
]

FIELD_PATTERN = re.compile(
    r"^(" + "|".join(re.escape(k) for k in FIELD_KEYS) + r")\s*:\s*(.*)$"
)


def _empty_row(prop_id: str, has_restaurant: str) -> dict:
    row = {col: "" for col in CSV_COLUMNS}
    row["Property ID"] = prop_id
    row["Does the hotel have an on site restaurant?"] = has_restaurant
    return row


def _parse_restaurant_block(block: str, prop_id: str, has_restaurant: str) -> dict:
    row = _empty_row(prop_id, has_restaurant)
    current_field = None
    current_lines = []

    def flush():
        if current_field:
            row[current_field] = "\n".join(current_lines).strip()

    for line in block.splitlines():
        m = FIELD_PATTERN.match(line)
        if m:
            flush()
            current_field = m.group(1)
            current_lines = [m.group(2).strip()]
        elif current_field:
            stripped = line.strip()
            if stripped:
                current_lines.append(stripped)

    flush()
    return row


def parse_output(text: str, prop_id: str) -> list[dict]:
    has_match = re.search(
        r"Does the hotel have an on site restaurant\?\s*(Yes|No)", text, re.IGNORECASE
    )
    has_restaurant = has_match.group(1).strip() if has_match else "No"

    if has_restaurant.lower() == "no":
        return [_empty_row(prop_id, "No")]

    block_starts = [m.start() for m in re.finditer(r"Restaurant Sequence\s*:\s*\d+", text)]

    if not block_starts:
        return [_empty_row(prop_id, has_restaurant)]

    rows = []
    for i, start in enumerate(block_starts):
        end = block_starts[i + 1] if i + 1 < len(block_starts) else len(text)
        block = text[start:end]
        rows.append(_parse_restaurant_block(block, prop_id, has_restaurant))

    return rows


def extract_hotel(hotel: dict) -> dict:
    prop_id = hotel["Property ID"]
    pages_text = load_pages_file(prop_id)
    source = "pages" if pages_text and len(pages_text) >= MIN_PAGES_CHARS else "search"

    raw_output = call_gemini(hotel, pages_text)
    rows = parse_output(raw_output, prop_id)

    return {
        "prop_id": prop_id,
        "status": "done",
        "source": source,
        "rows": rows,
        "raw_output": raw_output,
    }
