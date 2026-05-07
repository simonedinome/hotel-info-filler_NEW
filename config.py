from __future__ import annotations

import os
from pathlib import Path



def load_dotenv_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_dotenv_file()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")


#GOOGLE_API_KEY = "YOUR_KEY_HERE"
#OPENROUTER_API_KEY = "YOUR_KEY_HERE"

GEMINI_MODEL = "gemini-flash-latest"
OPENROUTER_MODEL = "openai/gpt-4o"

GEMINI_TEMPERATURE = 0.1
WRITER_TEMPERATURE = 0.4
GEMINI_MAX_TOKENS = 16384
WRITER_MAX_TOKENS = 4096

FIRECRAWL_MAX_DEPTH = 3
FIRECRAWL_PAGE_LIMIT = 50

MIN_CATEGORY_CHARS = 300
REQUEST_DELAY = 3
VERIFIER_RETRY_MAX = 3
WRITER_RETRY_MAX = 3

SEARCH_DOMAINS = [
    "{hotel_website}",
    "bestwestern.it",
    "book.bestwestern.it"
]

PAGES_DIR = "pages"
OUTPUT_DIR = "output"
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
INPUT_DIR = "input"
HOTELS_INPUT_PATH = str(Path(INPUT_DIR) / "export-hotel.csv")

CATEGORY_KEYWORDS = {
    "dining": [
        "restaurant",
        "bar",
        "dining",
        "food",
        "breakfast",
        "cuisine",
        "menu",
        "bistro",
        "cafe",
        "buffet",
        "lounge",
        "brasserie",
        "brunch",
        "lunch",
        "dinner",
        "ristorante",
        "colazione",
        "cucina",
        "pranzo",
        "cena",
        "tavolo",
    ],
    "spa": [
        "spa",
        "wellness",
        "massage",
        "treatment",
        "sauna",
        "hammam",
        "thermal",
        "facial",
        "body wrap",
        "relaxation",
        "hydrotherapy",
        "steam room",
        "massaggio",
        "trattamento",
        "benessere",
        "terme",
        "relax",
    ],
    "pool": [
        "pool",
        "swim",
        "swimming",
        "aqua",
        "water",
        "lazy river",
        "waterpark",
        "rooftop pool",
        "resort pool",
        "splash",
        "piscina",
        "nuoto",
        "vasca",
        "acquapark",
    ],
    "meetings": [
        "meeting",
        "event",
        "conference",
        "wedding",
        "banquet",
        "congress",
        "ballroom",
        "boardroom",
        "seminar",
        "co-working",
        "coworking",
        "venue",
        "sala",
        "riunione",
        "matrimonio",
        "evento",
        "convegno",
        "banchetto",
    ],
    "golf": [
        "golf",
        "course",
        "green",
        "driving range",
        "clubhouse",
        "fairway",
        "pro shop",
        "caddy",
        "tee",
        "bunker",
        "buca",
        "campo da golf",
        "campo golf",
    ],
    "experiences": [
        "beach",
        "casino",
        "marina",
        "fishing",
        "entertainment",
        "rooftop",
        "stargazing",
        "live music",
        "tennis",
        "basketball",
        "volleyball",
        "culinary",
        "cooking class",
        "wine tasting",
        "spiaggia",
        "pesca",
        "intrattenimento",
        "terrazza",
    ],
}

ALL_CATEGORIES = ["dining", "spa", "pool", "meetings", "golf", "experiences"]


def _normalize_cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    return str(value).strip()


def load_hotels(path: str | None = None) -> list[dict]:
    import csv

    csv_path = Path(path or HOTELS_INPUT_PATH)
    if not csv_path.exists():
        return []

    hotels = []
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel  # fallback to comma
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            if reader.fieldnames is None:
                return []
            for row in reader:
                prop_id = _normalize_cell(row.get("Property ID", ""))
                if not prop_id:
                    continue
                hotels.append({
                    "Property ID": prop_id,
                    "Nome account": _normalize_cell(row.get("Nome account", "")),
                    "Sito Web": _normalize_cell(row.get("Sito Web", "")),
                    "fLatitude": _normalize_cell(row.get("fLatitude", "")),
                    "fLongitude": _normalize_cell(row.get("fLongitude", "")),
                })
    except (IOError, OSError):
        return []

    return hotels


def hotels_by_id(path: str | None = None) -> dict[str, dict]:
    return {hotel["Property ID"]: hotel for hotel in load_hotels(path)}

def validate_api_keys() -> None:
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
