from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook


GOOGLE_API_KEY = "YOUR_KEY_HERE"
OPENROUTER_API_KEY = "YOUR_KEY_HERE"

GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
OPENROUTER_MODEL = "openai/gpt-4o"

GEMINI_TEMPERATURE = 0.1
WRITER_TEMPERATURE = 0.4
GEMINI_MAX_TOKENS = 8192
WRITER_MAX_TOKENS = 4096

MIN_CATEGORY_CHARS = 300
REQUEST_DELAY = 3
VERIFIER_RETRY_MAX = 3
WRITER_RETRY_MAX = 3

SEARCH_DOMAINS = [
    "{hotel_website}",
    "bestwestern.it",
    "book.bestwestern.it",
    "worldhotels.com",
]

PAGES_DIR = "pages"
OUTPUT_DIR = "output"
PROMPTS_DIR = "prompts"
SCHEMAS_DIR = "schemas"
INPUT_DIR = "input"
HOTELS_INPUT_PATH = str(Path(INPUT_DIR) / "export-hotel.xlsx")

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
    workbook_path = Path(path or HOTELS_INPUT_PATH)
    if not workbook_path.exists():
        return []
    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    rows = sheet.iter_rows(values_only=True)
    try:
        header = [str(cell).strip() if cell is not None else "" for cell in next(rows)]
    except StopIteration:
        workbook.close()
        return []
    indexes = {name: index for index, name in enumerate(header)}

    def cell(row_values, column_name: str):
        index = indexes.get(column_name)
        if index is None or index >= len(row_values):
            return ""
        return row_values[index]

    hotels = []
    for row in rows:
        prop_id = _normalize_cell(cell(row, "Property ID"))
        if not prop_id:
            continue
        hotels.append(
            {
                "Property ID": prop_id,
                "Nome account": _normalize_cell(cell(row, "Nome account")),
                "Sito Web": _normalize_cell(cell(row, "Sito Web")),
            }
        )
    workbook.close()
    return hotels


def hotels_by_id(path: str | None = None) -> dict[str, dict]:
    return {hotel["Property ID"]: hotel for hotel in load_hotels(path)}
