from __future__ import annotations

FIELD_TYPES = ("system", "factual", "enum", "editorial", "url", "email")


def column(
    key: str,
    field_type: str,
    *,
    required: bool = False,
    hardcoded_value=None,
    multi_select: bool = False,
    allowed_values: list[str] | None = None,
    description: str = "",
) -> dict:
    item = {
        "key": key,
        "field_type": field_type,
        "required": required,
        "description": description,
    }
    if hardcoded_value is not None:
        item["hardcoded_value"] = hardcoded_value
    if multi_select:
        item["multi_select"] = True
    if allowed_values is not None:
        item["allowed_values"] = allowed_values
    return item


def system_columns(property_key: str = "Property ID", tracking_key: str = "Tracking Status") -> list[dict]:
    return [
        column(
            property_key,
            "system",
            required=True,
            description="BWH property identifier",
        ),
        column(
            tracking_key,
            "system",
            required=True,
            hardcoded_value="Complete",
            description="Hardcoded workflow status",
        ),
    ]


def columns_by_key(columns: list[dict]) -> dict[str, dict]:
    return {column_item["key"]: column_item for column_item in columns}


def get_output_keys_for_element(schema_module, element_id: str) -> list[str]:
    element = schema_module.ELEMENTS[element_id]
    return [
        column_item["key"]
        for column_item in schema_module.COLUMNS
        if column_item["key"] in schema_module.REPEATED_COLUMN_KEYS
        or column_item["field_type"] == "system"
        or column_item["key"] in element["column_keys"]
    ]


def get_editorial_keys_for_element(schema_module, element_id: str) -> list[str]:
    keys = set(get_output_keys_for_element(schema_module, element_id))
    return [
        column_item["key"]
        for column_item in schema_module.COLUMNS
        if column_item["field_type"] == "editorial" and column_item["key"] in keys
    ]


def get_factual_keys_for_element(schema_module, element_id: str) -> list[str]:
    keys = set(get_output_keys_for_element(schema_module, element_id))
    return [
        column_item["key"]
        for column_item in schema_module.COLUMNS
        if column_item["field_type"] not in {"editorial", "system"} and column_item["key"] in keys
    ]


def get_verifiable_keys_for_element(schema_module, element_id: str) -> list[str]:
    """Return only factual-typed keys for an element — the subset the verifier should check."""
    keys = set(get_output_keys_for_element(schema_module, element_id))
    return [
        column_item["key"]
        for column_item in schema_module.COLUMNS
        if column_item["field_type"] == "factual" and column_item["key"] in keys
    ]
