from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sys

from config import OUTPUT_DIR


def create_run_log() -> str:
    run_dir = Path(OUTPUT_DIR) / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = run_dir / f"{timestamp}.log"
    path.touch(exist_ok=True)
    return str(path)


@dataclass
class CategoryLogger:
    prop_id: str
    hotel_name: str
    category: str
    run_log_path: str
    progress_label: str = ""

    def __post_init__(self) -> None:
        hotel_dir = Path(OUTPUT_DIR) / "hotels" / str(self.prop_id)
        hotel_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = hotel_dir / f"{self.category}-processing.log"

    def _prefix(self) -> str:
        base = f"[{self.prop_id} | {self.category.upper()}"
        if self.progress_label:
            base += f" | {self.progress_label}"
        return base + "]"

    def _write(self, level: str, msg: str) -> None:
        line = f"{self._prefix()} {level}{msg}"
        sys.stdout.write(line + "\n")
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        with Path(self.run_log_path).open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def info(self, msg: str) -> None:
        self._write("", msg)

    def warning(self, msg: str) -> None:
        self._write("WARNING: ", msg)

    def error(self, msg: str, exc: Exception | None = None) -> None:
        if exc is None:
            self._write("ERROR: ", msg)
            return
        self._write("ERROR: ", f"{msg} | {exc}")

    def success(self, msg: str) -> None:
        self._write("", f"SUCCESS: {msg}")

    def log_step(self, step: int, name: str) -> None:
        self.info(f"STEP {step} - {name}")

    def log_field_verified(self, field: str, value: str) -> None:
        self.info(f"Verified field: {field} = {value}")

    def log_field_rejected(self, field: str, value: str, reason: str) -> None:
        self.warning(f"Rejected field: {field} = {value} | {reason}")

    def log_component_active(self, component: str, active: bool) -> None:
        state = "active" if active else "inactive"
        self.info(f"Component {component}: {state}")

    def log_api_call(self, model: str, tokens_in: int, tokens_out: int) -> None:
        self.info(f"API {model} | in={tokens_in} out={tokens_out}")

    def log_writer_skipped(self, reason: str) -> None:
        self.info(f"Writer skipped: {reason}")

    def log_writer_failed(self, attempt: int, error: str) -> None:
        self.warning(f"Writer attempt {attempt} failed: {error}")

    def log_enum_confidence(self, field: str, value, confidence: float | None) -> None:
        score = f"{confidence:.2f}" if confidence is not None else "n/a"
        self.info(f"Enum confidence [{score}]: {field} = {value}")

    def log_grounding_diagnostics(self, segments_found: int, source_text_length: int, search_enabled: bool) -> None:
        self.info(
            f"Grounding diagnostics: segments={segments_found}, "
            f"source_text_length={source_text_length}, search_enabled={search_enabled}"
        )
