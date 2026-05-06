from schemas.common import column, system_columns


CATEGORY_NAME = "golf"

PRESENCE_KEYWORDS = [
    "golf",
    "course",
    "green",
    "driving range",
    "clubhouse",
    "fairway",
    "campo da golf",
]

COLUMNS = system_columns() + [
    column(
        "Type of Golf Experience",
        "enum",
        allowed_values=["On-site", "Nearby","Adjacent", "No golf onsite or near the hotel"],
    ),
    column(
        "Available Facilities",
        "enum",
        multi_select=True,
        allowed_values=[
            "1. None Available",
            "Pro Shop",
            "Pro-Shop",
            "Clubhouse",
            "Practice Greens",
            "Driving Range",
            "Club Rentals",
            "Cart Rental",
        ],
    ),
    column("Golf Course Address (if different from hotel)", "factual"),
    column("GOLF PAGE:  Facilities - Pro Shop  Headline", "editorial"),
    column("GOLF PAGE:  Facilities - Pro Shop Description", "editorial"),
    column("GOLF PAGE:  Facilities - Pro Shop Link", "url"),
    column("GOLF PAGE:  Facilities - Clubhouse  Headline", "editorial"),
    column("GOLF PAGE:  Facilities - Clubhouse Description", "editorial"),
    column("GOLF PAGE:  Facilities - Clubhouse Link", "url"),
    column("GOLF PAGE:  Facilities - Practice Greens  Headline", "editorial"),
    column("GOLF PAGE:  Facilities-Practice Greens Description", "editorial"),
    column("GOLF PAGE: Facilities - Practice Greens Link", "url"),
    column("Driving Range Headline", "editorial"),
    column("Driving Range Description", "editorial"),
    column("Driving Range Link", "url"),
    column("Club Rentals Headline", "editorial"),
    column("Club Rentals Description", "editorial"),
    column("Club Rentals Link", "url"),
    column("Cart Rental Headline", "editorial"),
    column("Cart Rental Description", "editorial"),
    column("Golf Cart Link", "url"),
    column("GOLF PAGE: Golf Headline", "editorial"),
    column("GOLF PAGE: Golf Description", "editorial"),
    column("GOLF PAGE: Golf Feature Headline", "editorial"),
    column("GOLF PAGE: Golf Feature Description", "editorial"),
    column("GOLF PAGE: Quote", "editorial"),
    column("GOLF PAGE: Attribute", "editorial"),
    column("OVERVIEW PAGE: Golf Headline", "editorial"),
    column("OVERVIEW PAGE: Golf Description", "editorial"),
    column("OVERVIEW PAGE: Golf Tip", "editorial"),
    column("EXPERIENCE PAGE: Golf Headline", "editorial"),
    column("EXPERIENCE PAGE: Golf Description", "editorial"),
    column("EXPERIENCE PAGE: Link to Golf Course Website", "url"),
]

ELEMENTS = {
    "golf_experience": {
        "label": "Golf Experience",
        "fallback_name": "Golf Experience",
        "identifier_columns": [],
        "column_keys": [],
    },
    "pro_shop": {
        "label": "Pro Shop",
        "fallback_name": "Pro Shop",
        "identifier_columns": [],
        "column_keys": [
            "GOLF PAGE:  Facilities - Pro Shop  Headline",
            "GOLF PAGE:  Facilities - Pro Shop Description",
            "GOLF PAGE:  Facilities - Pro Shop Link",
        ],
    },
    "clubhouse": {
        "label": "Clubhouse",
        "fallback_name": "Clubhouse",
        "identifier_columns": [],
        "column_keys": [
            "GOLF PAGE:  Facilities - Clubhouse  Headline",
            "GOLF PAGE:  Facilities - Clubhouse Description",
            "GOLF PAGE:  Facilities - Clubhouse Link",
        ],
    },
    "practice_greens": {
        "label": "Practice Greens",
        "fallback_name": "Practice Greens",
        "identifier_columns": [],
        "column_keys": [
            "GOLF PAGE:  Facilities - Practice Greens  Headline",
            "GOLF PAGE:  Facilities-Practice Greens Description",
            "GOLF PAGE: Facilities - Practice Greens Link",
        ],
    },
    "driving_range": {
        "label": "Driving Range",
        "fallback_name": "Driving Range",
        "identifier_columns": [],
        "column_keys": [
            "Driving Range Headline",
            "Driving Range Description",
            "Driving Range Link",
        ],
    },
    "club_rentals": {
        "label": "Club Rentals",
        "fallback_name": "Club Rentals",
        "identifier_columns": [],
        "column_keys": [
            "Club Rentals Headline",
            "Club Rentals Description",
            "Club Rentals Link",
        ],
    },
    "cart_rental": {
        "label": "Cart Rental",
        "fallback_name": "Cart Rental",
        "identifier_columns": [],
        "column_keys": [
            "Cart Rental Headline",
            "Cart Rental Description",
            "Golf Cart Link",
        ],
    },
}
