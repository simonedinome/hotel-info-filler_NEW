from schemas.common import column, system_columns


CATEGORY_NAME = "pool"

PRESENCE_KEYWORDS = [
    "pool",
    "swim",
    "swimming",
    "aqua",
    "water",
    "piscina",
    "nuoto",
    "vasca",
]

COLUMNS = system_columns() + [
    column(
        "Water Feature Type",
        "enum",
        multi_select=True,
        allowed_values=[
            "1. Resort-Style Pool Experience",
            "2. Resort Style Pool",
            "2. Resort-Style Pool",
            "3. Rooftop Pool Experience",
            "4. Lazy River",
            "5. Waterpark",
        ],
    ),
    column("OVERVIEW PAGE:  Resort-Style Pool Headline", "editorial"),
    column("OVERVIEW PAGE: Resort-Style Pool Description", "editorial"),
    column("Resort-Style Pool 'Local Tip'", "editorial"),
    column("EXPERIENCE PAGE: Resort-Style Pool Headline", "editorial"),
    column("EXPERIENCE PAGE: Resort-Style Pool Description", "editorial"),
    column("OVERVIEW PAGE: Rooftop Pool Headline", "editorial"),
    column("OVERVIEW PAGE: Rooftop Pool Description", "editorial"),
    column("OVERVIEW PAGE: Rooftop Pool Tip", "editorial"),
    column("EXPERIENCE PAGE: Rooftop Pool Headline", "editorial"),
    column("EXPERIENCE PAGE: Rooftop Pool Description", "editorial"),
    column("EXPERIENCE PAGE: Lazy River Headline", "editorial"),
    column("EXPERIENCE PAGE: Lazy River Description", "editorial"),
    column("EXPERIENCE PAGE: Waterpark Headline", "editorial"),
    column("EXPERIENCE PAGE: Waterpark Description", "editorial"),
]

REPEATED_COLUMN_KEYS = ["Water Feature Type"]

ELEMENTS = {
    "resort_style_pool": {
        "label": "Resort-Style Pool",
        "fallback_name": "Resort-Style Pool",
        "identifier_columns": [],
        "column_keys": [
            "OVERVIEW PAGE:  Resort-Style Pool Headline",
            "OVERVIEW PAGE: Resort-Style Pool Description",
            "Resort-Style Pool 'Local Tip'",
            "EXPERIENCE PAGE: Resort-Style Pool Headline",
            "EXPERIENCE PAGE: Resort-Style Pool Description",
        ],
    },
    "rooftop_pool": {
        "label": "Rooftop Pool",
        "fallback_name": "Rooftop Pool",
        "identifier_columns": [],
        "column_keys": [
            "OVERVIEW PAGE: Rooftop Pool Headline",
            "OVERVIEW PAGE: Rooftop Pool Description",
            "OVERVIEW PAGE: Rooftop Pool Tip",
            "EXPERIENCE PAGE: Rooftop Pool Headline",
            "EXPERIENCE PAGE: Rooftop Pool Description",
        ],
    },
    "lazy_river": {
        "label": "Lazy River",
        "fallback_name": "Lazy River",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Lazy River Headline",
            "EXPERIENCE PAGE: Lazy River Description",
        ],
    },
    "waterpark": {
        "label": "Waterpark",
        "fallback_name": "Waterpark",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Waterpark Headline",
            "EXPERIENCE PAGE: Waterpark Description",
        ],
    },
}
