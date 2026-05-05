import argparse
import json
import os
import sys
import time
import traceback

from config import HOTELS, HOTELS_BY_ID, OUTPUT_DIR, REQUEST_DELAY
from extractor import extract_hotel
from exporter import export_single, export_all

CHECKPOINT_PATH = os.path.join(OUTPUT_DIR, "checkpoint.json")


def load_checkpoint() -> dict:
    if not os.path.exists(CHECKPOINT_PATH):
        return {}
    with open(CHECKPOINT_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_checkpoint(results: dict):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def print_status(results: dict):
    total = len(HOTELS)
    done = sum(1 for v in results.values() if v["status"] == "done")
    errors = sum(1 for v in results.values() if v["status"] == "error")
    no_web = sum(1 for v in results.values() if v["status"] == "no-website")
    pending = total - done - errors - no_web
    print(f"\n{'─'*50}")
    print(f"  Total:      {total}")
    print(f"  Done:       {done}")
    print(f"  Errors:     {errors}")
    print(f"  No website: {no_web}")
    print(f"  Pending:    {pending}")
    print(f"{'─'*50}\n")


def process_one(prop_id: str, results: dict, force: bool = False) -> dict:
    hotel = HOTELS_BY_ID.get(prop_id)
    if not hotel:
        print(f"[ERROR] Property ID {prop_id} not found in config.")
        return results

    if not force and prop_id in results and results[prop_id]["status"] == "done":
        print(f"[SKIP]  {prop_id} already done. Use --force to reprocess.")
        return results

    if not hotel.get("Sito Web"):
        pages_path = os.path.join("pages", f"{prop_id}-pages.txt")
        if not os.path.exists(pages_path):
            print(f"[SKIP]  {prop_id} — no website and no pages file.")
            results[prop_id] = {"status": "no-website", "prop_id": prop_id, "rows": None}
            save_checkpoint(results)
            return results

    name = hotel["Nome account"]
    print(f"[RUN]   {prop_id} — {name}")

    try:
        result = extract_hotel(hotel)
        source_tag = f"[{result['source'].upper()}]"
        restaurant_count = len(result["rows"])
        has_restaurant = result["rows"][0].get("Does the hotel have an on site restaurant?", "?") if result["rows"] else "?"
        if has_restaurant.lower() == "no":
            print(f"[DONE]  {prop_id} {source_tag} — No onsite restaurant")
        else:
            print(f"[DONE]  {prop_id} {source_tag} — {restaurant_count} venue(s) found")
        results[prop_id] = result
    except Exception as e:
        print(f"[ERROR] {prop_id} — {e}")
        results[prop_id] = {
            "status": "error",
            "prop_id": prop_id,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "rows": None,
        }

    save_checkpoint(results)
    return results


def cmd_process_all(args):
    results = load_checkpoint()
    pending = [
        h for h in HOTELS
        if args.force or h["Property ID"] not in results or results[h["Property ID"]]["status"] in ("error", "no-website")
    ]

    if not args.force:
        pending = [
            h for h in HOTELS
            if h["Property ID"] not in results or results[h["Property ID"]]["status"] == "error"
        ]

    print(f"Processing {len(pending)} hotels (skipping already done)...")
    print_status(results)

    for i, hotel in enumerate(pending):
        results = process_one(hotel["Property ID"], results, force=args.force)
        if i < len(pending) - 1:
            time.sleep(REQUEST_DELAY)

    print("\nBatch complete.")
    print_status(results)


def cmd_process_id(args):
    results = load_checkpoint()
    for prop_id in args.ids:
        results = process_one(prop_id.strip(), results, force=args.force)
        time.sleep(1)
    print_status(results)


def cmd_export_all(args):
    results = load_checkpoint()
    try:
        path = export_all(results)
        print(f"[OK] Global export saved: {path}")
    except ValueError as e:
        print(f"[ERROR] {e}")


def cmd_export_id(args):
    results = load_checkpoint()
    for prop_id in args.ids:
        prop_id = prop_id.strip()
        if prop_id not in results:
            print(f"[ERROR] {prop_id} not in checkpoint. Process it first.")
            continue
        data = results[prop_id]
        if data["status"] != "done" or not data.get("rows"):
            print(f"[ERROR] {prop_id} status is '{data['status']}', cannot export.")
            continue
        path = export_single(prop_id, data["rows"])
        print(f"[OK]  {prop_id} exported: {path}")


def cmd_status(args):
    results = load_checkpoint()
    print_status(results)
    if args.verbose:
        for hotel in HOTELS:
            pid = hotel["Property ID"]
            name = hotel["Nome account"]
            if pid not in results:
                status = "pending"
                detail = ""
            else:
                r = results[pid]
                status = r["status"]
                if status == "done":
                    count = len(r.get("rows") or [])
                    has = (r["rows"][0].get("Does the hotel have an on site restaurant?", "") if r["rows"] else "")
                    detail = f"— No restaurant" if has.lower() == "no" else f"— {count} venue(s)"
                elif status == "error":
                    detail = f"— {r.get('error', '')[:60]}"
                else:
                    detail = ""
            print(f"  [{status.upper():12}] {pid}  {name[:40]}  {detail}")


def cmd_retry_errors(args):
    results = load_checkpoint()
    errors = [pid for pid, v in results.items() if v["status"] == "error"]
    if not errors:
        print("No errors to retry.")
        return
    print(f"Retrying {len(errors)} failed hotels...")
    for prop_id in errors:
        results = process_one(prop_id, results, force=True)
        time.sleep(REQUEST_DELAY)
    print_status(results)


def main():
    parser = argparse.ArgumentParser(
        prog="process.py",
        description="BWH Hotel Dining Extractor",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_all = sub.add_parser("process-all", help="Process all pending/error hotels")
    p_all.add_argument("--force", action="store_true", help="Reprocess already done hotels")
    p_all.set_defaults(func=cmd_process_all)

    p_id = sub.add_parser("process", help="Process one or more hotels by Property ID")
    p_id.add_argument("ids", nargs="+", metavar="PROP_ID")
    p_id.add_argument("--force", action="store_true")
    p_id.set_defaults(func=cmd_process_id)

    p_ex_all = sub.add_parser("export-all", help="Export all done hotels to single xlsx")
    p_ex_all.set_defaults(func=cmd_export_all)

    p_ex_id = sub.add_parser("export", help="Export one or more hotels to individual xlsx")
    p_ex_id.add_argument("ids", nargs="+", metavar="PROP_ID")
    p_ex_id.set_defaults(func=cmd_export_id)

    p_status = sub.add_parser("status", help="Show processing status")
    p_status.add_argument("-v", "--verbose", action="store_true")
    p_status.set_defaults(func=cmd_status)

    p_retry = sub.add_parser("retry-errors", help="Retry all hotels in error state")
    p_retry.set_defaults(func=cmd_retry_errors)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
