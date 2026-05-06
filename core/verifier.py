from __future__ import annotations

import json
from copy import deepcopy

from config import GEMINI_MODEL, VERIFIER_RETRY_MAX
from core.extractor import _extract_text, _search_domains, call_with_retry, get_gemini_client
from schemas.common import columns_by_key


def _verification_prompt(field_name: str, value, citation: str, source_text: str, hotel: dict, category: str, search_enabled: bool) -> str:
    search_instruction = ""
    if search_enabled:
        search_instruction = (
            f"\nAllowed search domains: {', '.join(_search_domains(hotel))}\n"
            "Google Search is enabled for this verification. If the local source text is empty or incomplete, "
            "you may verify using grounded search results from the allowed domains.\n"
        )
    return (
        "You are a strict fact-checker for hotel content.\n\n"
        f"Hotel name: {hotel.get('Nome account', '')}\n"
        f"Website: {hotel.get('Sito Web', '')}\n"
        f"Category: {category}\n"
        f"Field: {field_name}\n"
        f"Extracted value: {value}\n"
        f"Claimed citation: {citation}\n\n"
        f"Source text:\n{source_text}\n\n"
        f"{search_instruction}"
        'Return only JSON in this exact format: {"verdict":"YES","reason":"..."} or {"verdict":"NO","reason":"..."}.\n'
        'Answer YES only if the citation appears in the local source text or grounded search evidence and directly and explicitly supports the extracted value.'
    )


def verify_rows(raw_rows: list[dict], full_source_text: str, hotel: dict, category: str, schema_module, search_enabled: bool = False, logger=None) -> list[dict]:
    client, types = get_gemini_client()
    source_text = full_source_text or ""
    schema_columns = columns_by_key(schema_module.COLUMNS)
    verified_rows = deepcopy(raw_rows)
    for row in verified_rows:
        for field_name, payload in row.get("fields", {}).items():
            value = payload.get("value")
            citation = payload.get("citation")
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

            def run_call():
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=_verification_prompt(field_name, value, citation, source_text, hotel, category, search_enabled),
                    config={
                        "response_mime_type": "application/json",
                        **({"tools": [types.Tool(google_search=types.GoogleSearch())]} if search_enabled else {}),
                    },
                )
                return json.loads(_extract_text(response))

            verdict = call_with_retry(run_call, max_attempts=VERIFIER_RETRY_MAX, logger=logger)
            verdict_value = str(verdict.get("verdict", "")).upper().strip()
            reason = str(verdict.get("reason", "")).strip()
            if verdict_value != "YES":
                row["fields"][field_name] = {"value": None, "citation": None}
                if logger is not None:
                    logger.log_field_rejected(field_name, str(value), reason or json.dumps(verdict, ensure_ascii=False))
            elif logger is not None:
                logger.log_field_verified(field_name, str(value))
    return verified_rows
