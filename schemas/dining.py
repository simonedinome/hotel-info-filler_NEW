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
    column("Does the hotel have a on-site restuarant?", "enum", allowed_values=["Yes", "No"]),
    column("Restaurant Sequence - if multiple", "factual"),
    column("Restaurant Name", "factual"),
    column("Restaurant Type", "enum", multi_select=False, allowed_values= [
            "Restaurant",
            "Bar",
            "Café",
            "Lounge",
            "Bistro",
            "Rooftop Bar",
            "Poolside Bar",
            "Buffet Restaurant",
            "Steakhouse",
            "Seafood Restaurant",
            "Breakfast Only",
        ],),
    column("Phone Number", "factual"),
    column("Hours of Operation", "factual"),
    column("Fare / Cuisine Type", "enum", multi_select=False, allowed_values= [
            "American",
            "Italian",
            "Mediterranean",
            "International",
            "French",
            "Asian",
            "Japanese",
            "Chinese",
            "Indian",
            "Mexican",
            "Fusion",
            "Continental",
            "Regional/Local",
            "Steakhouse",
            "Seafood",
            "Pizza",
            "Vegetarian",
        ],),
    column(
        "Dietary Menu Options",
        "enum",
        multi_select=True,
        allowed_values=["1. Vegan", "2. Vegetarian", "3. Gluten Free", "4. None of the above"],
    ),
    column(
        "Meals Served",
        "enum",
        multi_select=True,
        allowed_values=["1. Breakfast", "2. Brunch", "3. Lunch", "4. Dinner"],
    ),
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
