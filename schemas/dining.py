from schemas.common import column, system_columns


CATEGORY_NAME = "dining"

PRESENCE_KEYWORDS = [
    "restaurant",
    "bar",
    "dining",
    "food",
    "breakfast",
    "cuisine",
    "menu",
    "ristorante",
    "colazione",
    "cucina",
]

COLUMNS = system_columns() + [
    column("Does the hotel have a on-site restuarant?", "enum"),
    column("Restaurant Sequence - if multiple", "factual"),
    column("Restaurant Name", "factual"),
    column("Restaurant Type", "factual"),
    column("Phone Number", "factual"),
    column("Hours of Operation", "factual"),
    column("Fare / Cuisine Type", "factual"),
    column("Dietary Menu Options", "enum", multi_select=True),
    column("Meals Served", "enum", multi_select=True),
    column("Restaurant Description", "editorial"),
    column("Book a Table", "url"),
    column("View Menu", "url"),
    column("Visit Website", "url"),
    column("Image URL", "url"),
    column("EXPERIENCE PAGE: Dining Headline", "editorial"),
    column("EXPERIENCE PAGE: Dining Description", "editorial"),
    column("DINING PAGE: Description", "editorial"),
]

REPEATED_COLUMN_KEYS = ["Does the hotel have a on-site restuarant?"]

ELEMENTS = {
    "dining_venue": {
        "label": "Dining Venue",
        "fallback_name": "Dining Venue",
        "identifier_columns": ["Restaurant Name", "Restaurant Sequence - if multiple"],
        "column_keys": [
            "Restaurant Sequence - if multiple",
            "Restaurant Name",
            "Restaurant Type",
            "Phone Number",
            "Hours of Operation",
            "Fare / Cuisine Type",
            "Dietary Menu Options",
            "Meals Served",
            "Restaurant Description",
            "Book a Table",
            "View Menu",
            "Visit Website",
            "Image URL",
            "EXPERIENCE PAGE: Dining Headline",
            "EXPERIENCE PAGE: Dining Description",
            "DINING PAGE: Description",
        ],
    },
}
