from __future__ import annotations

import json
import time
from pathlib import Path

from config import (
    GEMINI_MAX_TOKENS,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GOOGLE_API_KEY,
    PROMPTS_DIR,
    SEARCH_DOMAINS,
    VERIFIER_RETRY_MAX,
)
from core import PromptNotConfiguredError
from schemas.common import get_factual_keys_for_element, get_output_keys_for_element


_GEMINI_CLIENT = None


def load_prompt(filename: str) -> str:
    path = Path(PROMPTS_DIR) / filename
    content = path.read_text(encoding="utf-8")
    if "PROMPT NOT YET CONFIGURED" in content:
        raise PromptNotConfiguredError(f"Prompt file not configured: {path}")
    return content


def call_with_retry(fn, max_attempts: int, delay: float = 2.0, logger=None):
    rate_limit_attempts = 0
    attempt = 0
    while attempt < max_attempts or rate_limit_attempts < 5:
        try:
            return fn()
        except Exception as exc:
            is_rate_limit = "429" in str(exc)
            if is_rate_limit:
                rate_limit_attempts += 1
                if rate_limit_attempts >= 5:
                    raise
                wait = max(10.0, delay * (2 ** rate_limit_attempts))
            else:
                if attempt >= max_attempts - 1:
                    raise
                wait = delay * (2 ** attempt)
                attempt += 1
            if logger is not None:
                current = rate_limit_attempts if is_rate_limit else attempt
                total = 5 if is_rate_limit else max_attempts
                logger.warning(f"Attempt {current}/{total} failed: {exc}. Retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("Retry loop exhausted without result")


def get_gemini_client():
    global _GEMINI_CLIENT
    if _GEMINI_CLIENT is None:
        from google import genai
        from google.genai import types

        _GEMINI_CLIENT = (genai.Client(api_key=GOOGLE_API_KEY), types)
    return _GEMINI_CLIENT


def _search_domains(hotel: dict) -> list[str]:
    website = (hotel.get("Sito Web") or "").replace("https://", "").replace("http://", "").strip("/")
    return [domain.replace("{hotel_website}", website) for domain in SEARCH_DOMAINS if domain]


def _generate_json(prompt: str, search_enabled: bool):
    client, types = get_gemini_client()
    config = {
        "temperature": GEMINI_TEMPERATURE,
        "max_output_tokens": GEMINI_MAX_TOKENS,
        "response_mime_type": "application/json",
    }
    if search_enabled:
        config["tools"] = [types.Tool(google_search=types.GoogleSearch())]
    return client.models.generate_content(model=GEMINI_MODEL, contents=prompt, config=config)


def _extract_text(response) -> str:
    text = getattr(response, "text", None)
    if text:
        return text.strip()
    parts = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            value = getattr(part, "text", None)
            if value:
                parts.append(value)
    return "\n".join(parts).strip()


def detect_presence(hotel: dict, category: str, context: dict) -> str:
    prompt = load_prompt("presence_detection.txt").format(
        hotel_name=hotel.get("Nome account", ""),
        website=hotel.get("Sito Web", ""),
        context=context.get("filtered_text", ""),
        category=category,
        search_domains=", ".join(_search_domains(hotel)),
    )
    response = call_with_retry(
        lambda: _generate_json(prompt, search_enabled=context.get("use_search", False)),
        max_attempts=VERIFIER_RETRY_MAX,
    )
    payload = json.loads(_extract_text(response))
    result = str(payload.get("presence", "unknown")).lower().strip()
    if result not in {"present", "absent", "unknown"}:
        return "unknown"
    return result


def format_schema_for_prompt(schema_module) -> str:
    lines = []
    lines.append("Columns:")
    for column in schema_module.COLUMNS:
        line = f'- {column["key"]} [{column["field_type"]}]'
        if column.get("description"):
            line += f' - {column["description"]}'
        lines.append(line)
    lines.append("")
    lines.append("Element types:")
    for element_id, element in schema_module.ELEMENTS.items():
        factual_keys = ", ".join(get_factual_keys_for_element(schema_module, element_id))
        output_keys = ", ".join(get_output_keys_for_element(schema_module, element_id))
        lines.append(f'- {element_id}: {element["label"]} | factual columns: {factual_keys} | output columns: {output_keys}')
    return "\n".join(lines)


def _normalize_field_payload(field_value):
    if isinstance(field_value, dict):
        return {
            "value": field_value.get("value"),
            "citation": field_value.get("citation"),
        }
    return {"value": field_value, "citation": None}


def normalize_extracted_rows(schema_module, payload) -> list[dict]:
    raw_rows = payload.get("rows", payload) if isinstance(payload, dict) else payload
    if not isinstance(raw_rows, list):
        return []
    normalized_rows = []
    for raw_row in raw_rows:
        if not isinstance(raw_row, dict):
            continue
        element_id = raw_row.get("element_id") or raw_row.get("element_type") or raw_row.get("element")
        if element_id not in schema_module.ELEMENTS:
            continue
        element_name = raw_row.get("element_name") or raw_row.get("identifier") or schema_module.ELEMENTS[element_id]["fallback_name"]
        fields_payload = raw_row.get("fields", raw_row)
        row = {
            "__element_id": element_id,
            "__element_name": element_name,
            "fields": {},
        }
        for key in get_factual_keys_for_element(schema_module, element_id):
            if key in {"Property ID", "Property iD", "Tracking Status", "Tracking status"}:
                continue
            row["fields"][key] = _normalize_field_payload(fields_payload.get(key))
        normalized_rows.append(row)
    return normalized_rows


def extract_rows(hotel: dict, category: str, context: dict, schema_module) -> list[dict]:
    prompt = load_prompt(f"{category}_extraction.txt").format(
        hotel_name=hotel.get("Nome account", ""),
        website=hotel.get("Sito Web", ""),
        context=context.get("filtered_text", ""),
        category=category,
        schema_fields=format_schema_for_prompt(schema_module),
        search_domains=", ".join(_search_domains(hotel)),
    )
    response = call_with_retry(
        lambda: _generate_json(prompt, search_enabled=context.get("use_search", False)),
        max_attempts=VERIFIER_RETRY_MAX,
    )
    payload = json.loads(_extract_text(response))
    return normalize_extracted_rows(schema_module, payload)
