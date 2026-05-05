from __future__ import annotations

import json
from pathlib import Path

import requests

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    PROMPTS_DIR,
    WRITER_MAX_TOKENS,
    WRITER_RETRY_MAX,
    WRITER_TEMPERATURE,
)
from core import PromptNotConfiguredError, safe_format
from core.extractor import call_with_retry
from schemas.common import get_editorial_keys_for_element


def get_openrouter_headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }


def load_prompt(filename: str) -> str:
    path = Path(PROMPTS_DIR) / filename
    content = path.read_text(encoding="utf-8")
    if "PROMPT NOT YET CONFIGURED" in content:
        raise PromptNotConfiguredError(f"Prompt file not configured: {path}")
    return content


def _verified_payload(row: dict) -> dict:
    return {
        key: value
        for key, value in row.get("fields", {}).items()
        if value.get("value") not in (None, [], "")
    }


def write_editorial(row: dict, category_context: str, schema_module, hotel: dict, category: str, logger=None) -> dict:
    verified_payload = _verified_payload(row)
    if not verified_payload:
        if logger is not None:
            logger.log_writer_skipped("no verified factual fields for row")
        return {}

    element_id = row["__element_id"]
    prompt = safe_format(
        load_prompt(f"{category}_writer.txt"),
        hotel_name=hotel.get("Nome account", ""),
        website=hotel.get("Sito Web", ""),
        context=category_context,
        element_id=element_id,
        element_name=row.get("__element_name", ""),
        verified_facts=json.dumps(verified_payload, ensure_ascii=False, indent=2),
        editorial_fields=json.dumps(get_editorial_keys_for_element(schema_module, element_id), ensure_ascii=False, indent=2),
    )
    payload = {
        "model": OPENROUTER_MODEL,
        "temperature": WRITER_TEMPERATURE,
        "max_tokens": WRITER_MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
    }

    def run_call():
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=get_openrouter_headers(),
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    try:
        return call_with_retry(run_call, max_attempts=WRITER_RETRY_MAX, logger=logger)
    except Exception as exc:
        if logger is not None:
            logger.log_writer_failed(WRITER_RETRY_MAX, str(exc))
        return {}
