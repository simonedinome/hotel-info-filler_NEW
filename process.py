from __future__ import annotations

import argparse
import sys
import time
import traceback

from config import ALL_CATEGORIES, REQUEST_DELAY, hotels_by_id, load_hotels
from core import PromptNotConfiguredError
from core.checkpoint import (
    get_status,
    load_checkpoint,
    mark_done_multi,
    mark_error,
    mark_no_data,
    mark_no_website,
)
from core.context import prepare_context
from core.exporter import export_all, export_category
from core.extractor import detect_presence, extract_rows, load_prompt
from core.logger import CategoryLogger, create_run_log
from core.verifier import verify_rows
from core.writer import write_editorial
from schemas import load_schema


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BWH Content Extractor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    process_parser = subparsers.add_parser("process")
    process_parser.add_argument("property_id")
    process_parser.add_argument("--categories", nargs="+", choices=ALL_CATEGORIES, default=None)
    process_parser.add_argument("--force", action="store_true")

    process_all_parser = subparsers.add_parser("process-all")
    process_all_parser.add_argument("--categories", nargs="+", choices=ALL_CATEGORIES, default=None)
    process_all_parser.add_argument("--force", action="store_true")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--categories", nargs="+", choices=ALL_CATEGORIES, required=True)

    subparsers.add_parser("export-all")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("-v", "--verbose", action="store_true")
    status_parser.add_argument("--categories", nargs="+", choices=ALL_CATEGORIES, default=None)

    retry_parser = subparsers.add_parser("retry-errors")
    retry_parser.add_argument("--categories", nargs="+", choices=ALL_CATEGORIES, default=None)

    subparsers.add_parser("check-prompts")
    return parser.parse_args()


def selected_categories(args_categories: list[str] | None) -> list[str]:
    return args_categories or ALL_CATEGORIES


def check_prompts(categories: list[str] | None = None) -> list[str]:
    categories = categories or ALL_CATEGORIES
    missing = []
    try:
        load_prompt("presence_detection.txt")
    except PromptNotConfiguredError as exc:
        missing.append(str(exc))
    for category in categories:
        for suffix in ("extraction", "writer"):
            try:
                load_prompt(f"{category}_{suffix}.txt")
            except PromptNotConfiguredError as exc:
                missing.append(str(exc))
    return missing


def verified_count(row: dict) -> int:
    count = 0
    for payload in row.get("fields", {}).values():
        if payload.get("value") not in (None, [], ""):
            count += 1
    return count


def build_row(schema_module, hotel: dict, verified_row: dict, editorial: dict) -> dict:
    row = {}
    fields = verified_row.get("fields", {})
    for column in schema_module.COLUMNS:
        key = column["key"]
        if column["field_type"] == "system":
            if "Property" in key:
                row[key] = hotel.get("Property ID", "")
            else:
                row[key] = column.get("hardcoded_value", "Complete")
            continue
        if key in editorial:
            row[key] = editorial.get(key)
            continue
        value = fields.get(key, {}).get("value")
        if isinstance(value, list):
            row[key] = "\n".join(str(item) for item in value)
        else:
            row[key] = value
    return row


def _effective_source(context: dict, presence_used_search: bool, extraction_used_search: bool) -> str:
    if context.get("source") == "search_only":
        return "search"
    if presence_used_search or extraction_used_search:
        return "pages+search"
    return "pages"


def process_category(hotel: dict, category: str, run_log_path: str, progress_label: str, force: bool = False) -> None:
    prop_id = str(hotel["Property ID"])
    if not force and get_status(category, prop_id) in {"done", "no-data", "no-website"}:
        return

    logger = CategoryLogger(
        prop_id=prop_id,
        hotel_name=hotel.get("Nome account", ""),
        category=category,
        run_log_path=run_log_path,
        progress_label=progress_label,
    )
    schema_module = load_schema(category)
    try:
        logger.log_step(0, "LOAD CONTEXT")
        context = prepare_context(prop_id, category)
        if context["full_text"] is None and not hotel.get("Sito Web"):
            mark_no_website(category, prop_id, has_category=False, source="search", writer_failed=False)
            logger.warning("No pages file and no website configured")
            return

        logger.log_step(1, "PRESENCE DETECTION")
        presence = detect_presence(hotel, category, context)
        presence_used_search = context["use_search"]
        if presence == "unknown" and not context["use_search"]:
            context = dict(context)
            context["use_search"] = True
            presence = detect_presence(hotel, category, context)
            presence_used_search = True
        if presence == "unknown":
            presence = "absent"
            logger.warning("Presence remained unknown after search; treated as absent")

        if presence == "absent":
            mark_no_data(
                category,
                prop_id,
                has_category=False,
                source=_effective_source(context, presence_used_search, False),
                writer_failed=False,
            )
            logger.success("Category absent, saved checkpoint with zero rows")
            return

        logger.log_step(2, "ROW EXTRACTION")
        raw_rows = extract_rows(hotel, category, context, schema_module)
        extraction_used_search = context["use_search"]
        if not raw_rows:
            mark_no_data(
                category,
                prop_id,
                has_category=False,
                source=_effective_source(context, presence_used_search, extraction_used_search),
                writer_failed=False,
            )
            logger.warning("No elements extracted; saved checkpoint with zero rows")
            return

        logger.log_step(3, "LLM VERIFICATION")
        verified_rows = verify_rows(
            raw_rows=raw_rows,
            full_source_text=context["full_text"] or context["filtered_text"],
            logger=logger,
        )

        logger.log_step(4, "EDITORIAL WRITING")
        final_rows = []
        writer_failed = False
        for verified_row in verified_rows:
            editorial = write_editorial(
                row=verified_row,
                category_context=context["filtered_text"] or context["full_text"] or "",
                schema_module=schema_module,
                hotel=hotel,
                category=category,
                logger=logger,
            )
            if verified_count(verified_row) > 0 and not editorial:
                writer_failed = True
            final_rows.append(build_row(schema_module, hotel, verified_row, editorial))

        logger.log_step(5, "CHECKPOINT SAVE")
        mark_done_multi(
            category,
            prop_id,
            final_rows,
            has_category=True,
            source=_effective_source(context, presence_used_search, extraction_used_search),
            writer_failed=writer_failed,
            raw_extraction=raw_rows,
            verified_extraction=verified_rows,
        )
        logger.success(f"Done - saved {len(final_rows)} rows to checkpoint")
    except Exception as exc:
        error_traceback = traceback.format_exc()
        mark_error(category, prop_id, str(exc), error_traceback)
        logger.error("Category processing failed", exc)


def process_hotels(hotels: list[dict], categories: list[str], force: bool = False, retry_errors_only: bool = False) -> None:
    run_log_path = create_run_log()
    total = len(hotels)
    for hotel_index, hotel in enumerate(hotels, start=1):
        progress_label = f"{hotel_index}/{total}"
        for category in categories:
            if retry_errors_only and get_status(category, str(hotel["Property ID"])) != "error":
                continue
            process_category(hotel, category, run_log_path, progress_label, force=force)
        if hotel_index < total:
            time.sleep(REQUEST_DELAY)


def print_status(hotels: list[dict], categories: list[str], verbose: bool) -> None:
    totals = {}
    for category in categories:
        checkpoint = load_checkpoint(category)
        counts = {"done": 0, "no-data": 0, "error": 0, "no-website": 0, "pending": 0, "total": len(hotels)}
        for hotel in hotels:
            status = checkpoint.get(str(hotel["Property ID"]), {}).get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
        totals[category] = counts

    if verbose:
        for category in categories:
            for hotel in hotels:
                status = get_status(category, str(hotel["Property ID"]))
                sys.stdout.write(f'{category}\t{hotel["Property ID"]}\t{hotel["Nome account"]}\t{status}\n')
        return

    sys.stdout.write("BWH Content Extractor - Status\n")
    sys.stdout.write("CATEGORY\tTOTAL\tDONE\tNO-DATA\tNO-WEBSITE\tERROR\tPENDING\n")
    for category in categories:
        counts = totals[category]
        sys.stdout.write(
            f"{category}\t{counts['total']}\t{counts['done']}\t{counts['no-data']}\t"
            f"{counts['no-website']}\t{counts['error']}\t{counts['pending']}\n"
        )


def main() -> None:
    args = parse_args()
    categories = selected_categories(getattr(args, "categories", None))
    hotels = load_hotels()
    hotels_index = hotels_by_id()

    if args.command == "check-prompts":
        missing = check_prompts()
        if missing:
            raise SystemExit("\n".join(missing))
        sys.stdout.write("All prompts are configured.\n")
        return

    if args.command == "export-all":
        for path in export_all():
            sys.stdout.write(path + "\n")
        return

    if args.command == "export":
        for category in categories:
            sys.stdout.write(export_category(category) + "\n")
        return

    if args.command == "status":
        print_status(hotels, categories, args.verbose)
        return

    if args.command in {"process", "process-all", "retry-errors"}:
        missing = check_prompts(categories)
        if missing:
            raise SystemExit("\n".join(missing))

    if args.command == "process":
        hotel = hotels_index.get(args.property_id)
        if hotel is None:
            raise SystemExit(f"Property ID not found: {args.property_id}")
        process_hotels([hotel], categories, force=args.force)
        return

    if args.command == "process-all":
        process_hotels(hotels, categories, force=args.force)
        return

    if args.command == "retry-errors":
        process_hotels(hotels, categories, retry_errors_only=True)
        return


if __name__ == "__main__":
    main()
