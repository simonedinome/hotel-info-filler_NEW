from __future__ import annotations

import json
import traceback as traceback_module
from datetime import datetime, timezone
from pathlib import Path

from config import OUTPUT_DIR


def checkpoint_path(category: str) -> Path:
    return Path(OUTPUT_DIR) / f"checkpoint-{category}.json"


def load_checkpoint(category: str) -> dict:
    path = checkpoint_path(category)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_checkpoint(category: str, data: dict) -> None:
    path = checkpoint_path(category)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def get_status(category: str, prop_id: str) -> str:
    item = load_checkpoint(category).get(str(prop_id))
    if item is None:
        return "pending"
    return item.get("status", "pending")


def _base_entry(status: str, **extra) -> dict:
    entry = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    entry.update(extra)
    return entry


def mark_done(category: str, prop_id: str, rows: list[dict], **extra) -> None:
    checkpoint = load_checkpoint(category)
    checkpoint[str(prop_id)] = _base_entry("done", rows=rows, **extra)
    save_checkpoint(category, checkpoint)


def mark_done_single(category: str, prop_id: str, row: dict, **extra) -> None:
    mark_done(category, prop_id, [row], **extra)


def mark_done_multi(category: str, prop_id: str, rows: list[dict], **extra) -> None:
    mark_done(category, prop_id, rows, **extra)


def mark_done_empty(category: str, prop_id: str, rows: list[dict], **extra) -> None:
    """Save checkpoint as done_empty: presence was confirmed but all verified fields are null.

    has_category is kept True (presence was confirmed).
    The rows array is preserved intact for export (renders in light orange).

    Guard: will not overwrite an existing 'done' entry, since that would
    be a regression (done_empty is strictly weaker than done).
    """
    checkpoint = load_checkpoint(category)
    existing = checkpoint.get(str(prop_id), {})
    if existing.get("status") == "done":
        return
    checkpoint[str(prop_id)] = _base_entry("done_empty", rows=rows, **extra)
    save_checkpoint(category, checkpoint)


def mark_error(category: str, prop_id: str, error: str, traceback: str | None = None) -> None:
    checkpoint = load_checkpoint(category)
    # Future-proofing guard: if parallelism is ever introduced, refuse to clobber
    # a successful 'done' entry with an error from a concurrent retry run.
    existing = checkpoint.get(str(prop_id), {})
    assert existing.get("status") != "done", "Refusing to overwrite done status with error"
    checkpoint[str(prop_id)] = _base_entry(
        "error",
        error=error,
        traceback=traceback or traceback_module.format_exc(),
        rows=[],
    )
    save_checkpoint(category, checkpoint)


def mark_no_data(category: str, prop_id: str, **extra) -> None:
    checkpoint = load_checkpoint(category)
    checkpoint[str(prop_id)] = _base_entry("no-data", rows=[], **extra)
    save_checkpoint(category, checkpoint)


def mark_no_website(category: str, prop_id: str, **extra) -> None:
    checkpoint = load_checkpoint(category)
    checkpoint[str(prop_id)] = _base_entry("no-website", rows=[], **extra)
    save_checkpoint(category, checkpoint)
