from schemas.common import column, system_columns


CATEGORY_NAME = "experiences"

PRESENCE_KEYWORDS = [
    "beach",
    "casino",
    "marina",
    "fishing",
    "entertainment",
    "rooftop",
    "spiaggia",
    "pesca",
    "intrattenimento",
]

COLUMNS = system_columns(property_key="Property iD") + [
    column(
        "Select each experience your hotel offers",
        "enum",
        multi_select=True,
        allowed_values=[
            "Resort-style pool",
            "Rooftop pool experience",
            "On-property golf",
            "Wellness center",
            "Spa",
            "Casino",
            "Marina",
            "Culinary experience",
            "Stargazing",
            "Live entertainment",
            "Rooftop dining or bars",
            "Beach access",
            "Fishing",
            "On-site tennis",
            "On-site basketball",
            "On-site pickleball",
            "On-site racquetball",
            "On-site Squash",
            "On-site volleyball",
            "No experiences at this hotel"
        ],
    ),
    column("Experience Page Description", "editorial"),
    column("EXPERIENCE PAGE: Beach Access Headline", "editorial"),
    column("EXPERIENCE PAGE: Beach Access Description", "editorial"),
    column("EXPERIENCE PAGE: Casino Headline", "editorial"),
    column("EXPERIENCE PAGE: Casino Description", "editorial"),
    column("EXPERIENCE PAGE: Co-working options Headline", "editorial"),
    column("EXPERIENCE PAGE: Co-working options Description", "editorial"),
    column("EXPERIENCE PAGE: Culinary Headline", "editorial"),
    column("EXPERIENCE PAGE: Culinary Description", "editorial"),
    column("EXPERIENCE PAGE - Fishing Headline", "editorial"),
    column("EXPERIENCE PAGE: Fishing Description", "editorial"),
    column("EXPERIENCE PAGE: Live Entertainment Headline", "editorial"),
    column("EXPERIENCE PAGE: Live Entertainment Description", "editorial"),
    column("EXPERIENCE PAGE: Marina Headline", "editorial"),
    column("EXPERIENCE PAGE: Marina Description", "editorial"),
    column("EXPERIENCE PAGE - Outdoor Recreation Headline", "editorial"),
    column("EXPERIENCE PAGE: Outdoor Recreation Description", "editorial"),
    column("EXPERIENCE PG: Rooftop Dining/Expr. Bars Headline", "editorial"),
    column("EXPERIENCE PG: Rooftop Dining & Bars Description", "editorial"),
    column("EXPERIENCE PAGE: Stargazing Headline", "editorial"),
    column("EXPERIENCE PAGE: Stargazing Description", "editorial"),
]


REPEATED_COLUMN_KEYS = ["Select each experience your hotel offers", "Experience Page Description"]

ELEMENTS = {
    "beach_access": {
        "label": "Beach access",
        "fallback_name": "Beach access",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Beach Access Headline",
            "EXPERIENCE PAGE: Beach Access Description",
        ],
    },
    "casino": {
        "label": "Casino",
        "fallback_name": "Casino",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Casino Headline",
            "EXPERIENCE PAGE: Casino Description",
        ],
    },
    "coworking_options": {
        "label": "Co-working options",
        "fallback_name": "Co-working options",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Co-working options Headline",
            "EXPERIENCE PAGE: Co-working options Description",
        ],
    },
    "culinary": {
        "label": "Culinary experience",
        "fallback_name": "Culinary experience",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Culinary Headline",
            "EXPERIENCE PAGE: Culinary Description",
        ],
    },
    "fishing": {
        "label": "Fishing",
        "fallback_name": "Fishing",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE - Fishing Headline",
            "EXPERIENCE PAGE: Fishing Description",
        ],
    },
    "live_entertainment": {
        "label": "Live Entertainment",
        "fallback_name": "Live Entertainment",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Live Entertainment Headline",
            "EXPERIENCE PAGE: Live Entertainment Description",
        ],
    },
    "marina": {
        "label": "Marina",
        "fallback_name": "Marina",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Marina Headline",
            "EXPERIENCE PAGE: Marina Description",
        ],
    },
    "outdoor_recreation": {
        "label": "Outdoor Recreation",
        "fallback_name": "Outdoor Recreation",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE - Outdoor Recreation Headline",
            "EXPERIENCE PAGE: Outdoor Recreation Description",
        ],
    },
    "rooftop_dining_bars": {
        "label": "Rooftop Dining/Expr. Bars",
        "fallback_name": "Rooftop Dining/Expr. Bars",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PG: Rooftop Dining/Expr. Bars Headline",
            "EXPERIENCE PG: Rooftop Dining & Bars Description",
        ],
    },
    "stargazing": {
        "label": "Stargazing",
        "fallback_name": "Stargazing",
        "identifier_columns": [],
        "column_keys": [
            "EXPERIENCE PAGE: Stargazing Headline",
            "EXPERIENCE PAGE: Stargazing Description",
        ],
    },
}
