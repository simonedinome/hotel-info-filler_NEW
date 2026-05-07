from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

from config import GEMINI_MODEL, VERIFIER_RETRY_MAX
from core.extractor import (
    _parse_json_response_text,
    _extract_text,
    _search_domains,
    bump_api_counter,
    call_with_retry,
    get_gemini_client,
)
from schemas.common import columns_by_key


VERIFIER_MAX_WORKERS = 8


def _verification_prompt_batch(
    fields_to_verify: list[dict],
    source_text: str,
    hotel: dict,
    category: str,
    search_enabled: bool,
) -> str:
    search_instruction = ""
    if search_enabled:
        search_instruction = (
            f"\nAllowed search domains: {', '.join(_search_domains(hotel))}\n"
            "Google Search is enabled for this verification. If the local source text is empty or incomplete, "
            "you may verify using grounded search results from the allowed domains.\n"
        )

    field_lines = []
    for idx, item in enumerate(fields_to_verify, start=1):
        field_lines.append(
            f'{idx}. field: "{item["field_name"]}"\n'
            f'   extracted_value: {json.dumps(item["value"], ensure_ascii=False)}\n'
            f'   claimed_citation: {json.dumps(item["citation"], ensure_ascii=False)}'
        )
    fields_block = "\n".join(field_lines)

    return (
        "You are a strict fact-checker for hotel content.\n\n"
        f"Hotel name: {hotel.get('Nome account', '')}\n"
        f"Website: {hotel.get('Sito Web', '')}\n"
        f"Category: {category}\n\n"
        f"Source text:\n{source_text}\n\n"
        f"{search_instruction}"
        "Verify each of the following extracted fields independently. "
        "For each field answer YES only if the citation appears in the local source text "
        "or grounded search evidence and directly and explicitly supports the extracted value. "
        "Otherwise answer NO.\n\n"
        f"Fields to verify:\n{fields_block}\n\n"
        'Return only JSON in this exact format: '
        '{"verdicts": [{"field": "<field_name>", "verdict": "YES" | "NO", "reason": "..."}, ...]}.\n'
        "Include exactly one entry per field, using the exact field name as provided."
    )


def _collect_fields_to_verify(row: dict, schema_columns: dict, logger) -> list[dict]:
    """Pull the factual fields that need an LLM verdict; log skipped non-factual fields inline."""
    pending = []
    for field_name, payload in row.get("fields", {}).items():
        value = payload.get("value")
        if value in (None, [], ""):
            continue
        col_def = schema_columns.get(field_name, {})
        field_type = col_def.get("field_type", "factual")
        if field_type != "factual":
            if field_type == "enum":
                if logger is not None:
                    logger.log_enum_confidence(field_name, value, payload.get("confidence"))
            else:
                if logger is not None:
                    logger.info(f"Skipping verification for {field_type} field: {field_name}")
            continue
        pending.append({
            "field_name": field_name,
            "value": value,
            "citation": payload.get("citation"),
        })
    return pending


def _verify_row(
    row: dict,
    source_text: str,
    hotel: dict,
    category: str,
    schema_columns: dict,
    search_enabled: bool,
    logger,
) -> None:
    """Verify all factual fields of a single row in one Gemini call. Mutates row in place."""
    pending = _collect_fields_to_verify(row, schema_columns, logger)
    if not pending:
        return

    client, types = get_gemini_client()

    def run_call():
        config = {"response_mime_type": "application/json"}
        if search_enabled:
            # Grounding tools are incompatible with response_mime_type — drop it when search is on.
            config = {"tools": [types.Tool(google_search=types.GoogleSearch())]}
        bump_api_counter()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=_verification_prompt_batch(pending, source_text, hotel, category, search_enabled),
            config=config,
        )
        return _parse_json_response_text(_extract_text(response))

    payload = call_with_retry(run_call, max_attempts=VERIFIER_RETRY_MAX, logger=logger)
    verdicts_list = payload.get("verdicts") if isinstance(payload, dict) else None
    if not isinstance(verdicts_list, list):
        verdicts_list = []

    verdicts_by_field = {}
    for entry in verdicts_list:
        if not isinstance(entry, dict):
            continue
        name = entry.get("field")
        if isinstance(name, str):
            verdicts_by_field[name] = entry

    for item in pending:
        field_name = item["field_name"]
        verdict = verdicts_by_field.get(field_name, {})
        verdict_value = str(verdict.get("verdict", "")).upper().strip()
        reason = str(verdict.get("reason", "")).strip()
        if verdict_value != "YES":
            row["fields"][field_name] = {"value": None, "citation": None}
            if logger is not None:
                logger.log_field_rejected(
                    field_name,
                    str(item["value"]),
                    reason or json.dumps(verdict, ensure_ascii=False) or "no verdict returned",
                )
        else:
            if logger is not None:
                logger.log_field_verified(field_name, str(item["value"]))


def verify_rows(
    raw_rows: list[dict],
    full_source_text: str,
    hotel: dict,
    category: str,
    schema_module,
    search_enabled: bool = False,
    logger=None,
) -> list[dict]:
    source_text = full_source_text or ""
    schema_columns = columns_by_key(schema_module.COLUMNS)
    verified_rows = deepcopy(raw_rows)
    if not verified_rows:
        return verified_rows

    max_workers = min(len(verified_rows), VERIFIER_MAX_WORKERS)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                _verify_row,
                row,
                source_text,
                hotel,
                category,
                schema_columns,
                search_enabled,
                logger,
            )
            for row in verified_rows
        ]
        for future in futures:
            future.result()
    return verified_rows
