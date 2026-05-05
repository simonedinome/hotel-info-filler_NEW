from schemas.common import column, system_columns


CATEGORY_NAME = "meetings"

PRESENCE_KEYWORDS = [
    "meeting",
    "event",
    "conference",
    "wedding",
    "banquet",
    "congress",
    "sala",
    "riunione",
    "matrimonio",
    "evento",
]

COLUMNS = system_columns(tracking_key="Tracking status") + [
    column("Meetings and Events facilities & space options", "enum", multi_select=True),
    column("Amenities & Services available", "enum", multi_select=True),
    column("Occasions ROUTINELY hosted at the hotel", "enum", multi_select=True),
    column("Enter hotel email address to send inquiries", "email"),
    column("FAQ #1: What types of spaces are available?", "factual"),
    column("FAQ #2:What are the rental fees, what is included?", "factual"),
    column("FAQ #3:  Do you offer catering services?", "factual"),
    column("FAQ #4:  Is there on-site technology support?", "factual"),
    column("FAQ #5:  Do you provide event planning assistance?", "factual"),
    column("Supplemental FAQ #1: Enter a question here", "factual"),
    column("Supplemental FAQ #1: Enter the answer FAQ #1", "factual"),
    column("Supplemental FAQ #2: Enter a question here", "factual"),
    column("Supplemental FAQ #2: Enter the answer FAQ #2", "factual"),
    column("Supplemental FAQ #3: Enter a question here", "factual"),
    column("Supplemental FAQ #3: Enter the answer FAQ #3", "factual"),
    column("Supplemental FAQ #4: Enter a question here", "factual"),
    column("Supplemental FAQ #4: Enter the answer FAQ #4", "factual"),
    column("MEETINGS & EVENTS PAGE: Headline", "editorial"),
    column("MEETINGS & EVENTS PAGE: Description", "editorial"),
    column("Guest or insider quote", "editorial"),
    column("Quote Attribute", "editorial"),
    column("OVERVIEW PAGE:  Meetings & Events Headline", "editorial"),
    column("OVERVIEW PAGE:  Meeting Space Description", "editorial"),
    column("MEETINGS & EVENTS PAGE:  Weddings Headline", "editorial"),
    column("MEETINGS & EVENTS PAGE:  Weddings Description", "editorial"),
    column("MEETINGS & EVENTS PAGE: Co-working Headline", "editorial"),
    column("MEETINGS & EVENTS PAGE: Co-working Description", "editorial"),
    column("MEETINGS & EVENTS PAGE: Event Space Description", "editorial"),
]

REPEATED_COLUMN_KEYS = [
    "Meetings and Events facilities & space options",
    "Amenities & Services available",
    "Occasions ROUTINELY hosted at the hotel",
    "Enter hotel email address to send inquiries",
    "FAQ #1: What types of spaces are available?",
    "FAQ #2:What are the rental fees, what is included?",
    "FAQ #3:  Do you offer catering services?",
    "FAQ #4:  Is there on-site technology support?",
    "FAQ #5:  Do you provide event planning assistance?",
    "Supplemental FAQ #1: Enter a question here",
    "Supplemental FAQ #1: Enter the answer FAQ #1",
    "Supplemental FAQ #2: Enter a question here",
    "Supplemental FAQ #2: Enter the answer FAQ #2",
    "Supplemental FAQ #3: Enter a question here",
    "Supplemental FAQ #3: Enter the answer FAQ #3",
    "Supplemental FAQ #4: Enter a question here",
    "Supplemental FAQ #4: Enter the answer FAQ #4",
    "MEETINGS & EVENTS PAGE: Headline",
    "MEETINGS & EVENTS PAGE: Description",
    "Guest or insider quote",
    "Quote Attribute",
    "OVERVIEW PAGE:  Meetings & Events Headline",
    "OVERVIEW PAGE:  Meeting Space Description",
    "MEETINGS & EVENTS PAGE: Event Space Description",
]

ELEMENTS = {
    "meetings_and_events": {
        "label": "Meetings and Events",
        "fallback_name": "Meetings and Events",
        "identifier_columns": [],
        "column_keys": [],
    },
    "business_meetings_and_events": {
        "label": "Host Business Meetings & Events",
        "fallback_name": "Host Business Meetings & Events",
        "identifier_columns": [],
        "column_keys": [],
    },
    "special_events": {
        "label": "Host Special Events",
        "fallback_name": "Host Special Events",
        "identifier_columns": [],
        "column_keys": [],
    },
    "ballroom_special_events": {
        "label": "Ballroom for Special Events",
        "fallback_name": "Ballroom for Special Events",
        "identifier_columns": [],
        "column_keys": [],
    },
    "weddings": {
        "label": "Wedding Space & Services",
        "fallback_name": "Wedding Space & Services",
        "identifier_columns": [],
        "column_keys": [
            "MEETINGS & EVENTS PAGE:  Weddings Headline",
            "MEETINGS & EVENTS PAGE:  Weddings Description",
        ],
    },
    "coworking": {
        "label": "Co-working Spaces",
        "fallback_name": "Co-working Spaces",
        "identifier_columns": [],
        "column_keys": [
            "MEETINGS & EVENTS PAGE: Co-working Headline",
            "MEETINGS & EVENTS PAGE: Co-working Description",
        ],
    },
}
