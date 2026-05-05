from __future__ import annotations

from copy import deepcopy

from config import GEMINI_MODEL, VERIFIER_RETRY_MAX
from core.extractor import _extract_text, call_with_retry, get_gemini_client


def _verification_prompt(field_name: str, value, citation: str, source_text: str) -> str:
    return (
        "You are a strict fact-checker for hotel content.\n\n"
        f"Field: {field_name}\n"
        f"Extracted value: {value}\n"
        f"Claimed citation: {citation}\n\n"
        f"Source text:\n{source_text}\n\n"
        "Does the claimed citation appear in the source text and directly and explicitly "
        'support the extracted value? Answer only "YES" or "NO" followed by one sentence explaining why.'
    )


def verify_rows(raw_rows: list[dict], full_source_text: str, logger=None) -> list[dict]:
    client, _ = get_gemini_client()
    source_text = full_source_text or ""
    verified_rows = deepcopy(raw_rows)
    for row in verified_rows:
        for field_name, payload in row.get("fields", {}).items():
            value = payload.get("value")
            citation = payload.get("citation")
            if value in (None, [], ""):
                continue

            def run_call():
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=_verification_prompt(field_name, value, citation, source_text),
                )
                return _extract_text(response)

            verdict = call_with_retry(run_call, max_attempts=VERIFIER_RETRY_MAX, logger=logger)
            if not verdict.upper().startswith("YES"):
                row["fields"][field_name] = {"value": None, "citation": None}
                if logger is not None:
                    logger.log_field_rejected(field_name, str(value), verdict)
            elif logger is not None:
                logger.log_field_verified(field_name, str(value))
    return verified_rows
