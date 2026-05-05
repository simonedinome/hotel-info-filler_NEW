# BWH Content Extractor - CODEX.md

## Read This File Before Writing Code

This document is the source of truth for the project.
If code and document conflict, update the code to match this file.

---

## 1. Project Overview

This project extracts structured hotel content from hotel websites and produces Excel files
ready for import into the BWH CMS.

Input sources:
- `pages/PROPID-pages.txt`
- Google Search when local context is weak
- `input/export-hotel.xlsx` for the hotel master list

Output:
- One Excel file per category
- One CSV file per category
- One checkpoint JSON file per category
- Logs per run and per hotel/category

Categories:
- `dining`
- `spa`
- `pool`
- `meetings`
- `golf`
- `experiences`

---

## 2. Business Rules

### Anti-hallucination
- Never populate a factual field without a verified citation.
- Never infer a facility from hotel brand, market, star rating, or hotel type.
- Never write quote fields unless the quote is verbatim in source text.
- Never mark a category absent only because `pages.txt` is weak.
- Never call the writer when verified factual content for a row is zero.

### Output modeling
- Every category is multi-row.
- Every output row represents one single element.
- If a category has zero elements for a hotel, export zero rows for that hotel in that category.
- `Property ID` and `Tracking Status` repeat on every row for the same hotel.
- `Tracking Status` is always hardcoded to `Complete`.

### Element granularity
- `dining`: one row per venue
- `spa`: one row per element
- `pool`: one row per water feature
- `meetings`: one row per named venue, room, or experience
- `golf`: one row per golf element
- `experiences`: one row per experience

### Template fidelity
- Output column names must stay identical to the CMS templates, including typos and spacing.
- Only real CMS columns are exported.
- Ignore helper columns such as `character count`, `count1`, `count2`, `format check`.
- Ignore template example data completely.
- Ignore the `Comments` worksheet in template files.

### Meetings special rule
- `Meeting & Events Capacity Details.xlsx` is ignored.
- Only `Meetings & Events form.xlsx` matters for this project.

---

## 3. Project Structure

```text
hotel-info-filler-new/
|
|-- CODEX.md
|-- config.py
|-- process.py
|-- requirements.txt
|
|-- input/
|   |-- export-hotel.xlsx
|
|-- pages/
|   |-- PROPID-pages.txt
|
|-- prompts/
|   |-- presence_detection.txt
|   |-- dining_extraction.txt
|   |-- dining_writer.txt
|   |-- spa_extraction.txt
|   |-- spa_writer.txt
|   |-- pool_extraction.txt
|   |-- pool_writer.txt
|   |-- meetings_extraction.txt
|   |-- meetings_writer.txt
|   |-- golf_extraction.txt
|   |-- golf_writer.txt
|   |-- experiences_extraction.txt
|   |-- experiences_writer.txt
|
|-- schemas/
|   |-- dining.py
|   |-- spa.py
|   |-- pool.py
|   |-- meetings.py
|   |-- golf.py
|   |-- experiences.py
|   |-- common.py
|
|-- core/
|   |-- context.py
|   |-- extractor.py
|   |-- verifier.py
|   |-- writer.py
|   |-- exporter.py
|   |-- checkpoint.py
|   |-- logger.py
|
|-- output/
|   |-- checkpoint-*.json
|   |-- bwh-*-export-YYYY-MM-DD.xlsx
|   |-- bwh-*-export-YYYY-MM-DD.csv
|   |-- run/
|   |-- hotels/
```

---

## 4. Input Files

### Hotel master list
- Source file: `input/export-hotel.xlsx`
- First sheet only
- Required columns:
  - `Property ID`
  - `Nome account`
  - `Sito Web`

This file is read at runtime.
Hotels are not hardcoded in `config.py`.

### CMS templates used to define schemas
- `Dining Intake Form.xlsx`
- `SPA Intake Form.xlsx`
- `Pool & Water Feature Form.xlsx`
- `Meetings & Events form.xlsx`
- `Golf Intake Form.xlsx`
- `Experiences Intake Form.xlsx`

These files define column names and row shape only.
Their sample data must never be reused as business data.

---

## 5. Processing Flow

Process one hotel at a time and one category at a time.
No parallelism.

### Step 0 - Load Context
- Read `pages/PROPID-pages.txt`
- Filter by category keywords
- If filtered context is weak, allow search fallback
- If pages file is missing and hotel website is empty, mark `no-website`

### Step 1 - Presence Detection
- Model: Gemini 2.5 Flash
- Prompt: `prompts/presence_detection.txt`
- Output: `present`, `absent`, or `unknown`

Rules:
- If `unknown` without search, rerun with search
- If still `unknown`, treat as `absent`
- If `absent`, checkpoint the category with zero rows

### Step 2 - Row Extraction
- Model: Gemini 2.5 Flash
- Prompt: `prompts/CATEGORY_extraction.txt`
- Function: `extract_rows()`

Expected extraction shape:

```json
{
  "rows": [
    {
      "element_id": "rooftop_pool",
      "element_name": "Rooftop Pool",
      "fields": {
        "Water Feature Type": {"value": ["3. Rooftop Pool Experience"], "citation": "..."},
        "OVERVIEW PAGE: Rooftop Pool Headline": {"value": "...", "citation": "..."}
      }
    }
  ]
}
```

Rules:
- One extracted object per element
- If a category has no elements, extraction returns an empty list
- Repeated category-level fields may appear on multiple rows
- Enum values must match the allowed values defined in the schema when present
- When Google Search is used, capture grounded support text for downstream verification whenever available

### Step 3 - Field Verification
- Model: Gemini 2.5 Flash
- Function: `verify_rows()`
- JSON response mode required
- Search enabled when extraction used Google Search or when local source text is insufficient

For every populated field in every extracted row:
- Check whether the citation explicitly supports the value
- If not, null out value and citation
- Verifier must return structured JSON such as `{"verdict":"YES","reason":"..."}` or `{"verdict":"NO","reason":"..."}`

### Step 4 - Editorial Writing
- Model: GPT-4o via OpenRouter
- Function: `write_editorial()`
- One writer call per row

Rules:
- Writer is row-level, not category-level
- Writer only receives the editorial fields relevant to that row element
- If verified factual fields for a row are zero, skip writer for that row
- On failure after max retries, keep editorial fields empty

### Step 5 - Row Assembly and Checkpoint Save
- Assemble final CMS rows in exact schema order
- Save `rows: list[dict]` for every category

Checkpoint entry example:

```json
{
  "98323": {
    "status": "done",
    "has_category": true,
    "source": "pages",
    "writer_failed": false,
    "rows": [
      {
        "Property ID": "98323",
        "Tracking Status": "Complete"
      }
    ],
    "timestamp": "2026-05-05T12:00:00Z"
  }
}
```

If absent:
- status = `no-data`
- rows = `[]`

If no website and no pages:
- status = `no-website`
- rows = `[]`

---

## 6. Schema Rules

Every schema file must define:
- `CATEGORY_NAME`
- `PRESENCE_KEYWORDS`
- `COLUMNS`
- `REPEATED_COLUMN_KEYS`
- `ELEMENTS`

`COLUMNS` contains only real CMS columns to export.

`ELEMENTS` maps the row model for that category.
Each element contains:
- label
- fallback name
- identifier columns
- column keys specific to that element

Repeated fields:
- stay in `REPEATED_COLUMN_KEYS`
- may be duplicated across multiple rows of the same hotel

Enum fields:
- should populate `allowed_values` whenever the CMS template defines a constrained set
- extraction prompts must show allowed enum values to the model

System fields:
- `Property ID` or `Property iD`
- `Tracking Status` or `Tracking status`

These are always generated by code, not extracted.

---

## 7. Category Modeling

### Dining
- One row per dining venue
- Use the exact template columns from `Dining Intake Form.xlsx`

### Spa
- One row per spa element
- General spa fields may repeat
- Component fields are filled only for the current row element

### Pool
- One row per water feature
- Fill only the columns for the current feature on that row

### Meetings
- One row per named venue, room, or experience
- If no real name exists, use the experience type as the identifier

### Golf
- One row per golf element
- Nearby golf is valid if explicitly confirmed by source

### Experiences
- One row per experience
- If no explicit element name exists, use the experience type itself

---

## 8. Prompt Files

Prompt files are authored by the user.
Code must never modify them.

Every prompt file must exist.
If any prompt file still contains the placeholder string, raise `PromptNotConfiguredError`
before any API call.

Placeholder content:

```text
[PROMPT NOT YET CONFIGURED - USER MUST FILL THIS FILE BEFORE RUNNING]
```

---

## 9. Checkpoints

One checkpoint file per category:
- `output/checkpoint-dining.json`
- `output/checkpoint-spa.json`
- `output/checkpoint-pool.json`
- `output/checkpoint-meetings.json`
- `output/checkpoint-golf.json`
- `output/checkpoint-experiences.json`

Writes must be atomic.

Resume behavior:
- `done`: skip
- `no-data`: skip
- `no-website`: skip
- `error`: retry from step 0
- missing entry: process from step 0

---

## 10. Export Rules

One Excel output per category.
One CSV output per category.

All categories export `rows` from checkpoints.
There is no single-row category anymore.

Formatting:
- header fill `1A1A2E`
- header font `F0A500`
- bold headers
- freeze first row
- alternating white and light grey for completed rows
- amber for `has_category: false`
- red for error-only lines if shown
- wrap text and top-align all cells
- auto-size columns with min 14 and max 60

---

## 11. CLI Commands

```bash
python process.py process 98435
python process.py process 98435 --categories spa pool
python process.py process-all
python process.py process-all --categories spa meetings golf
python process.py process 98435 --force
python process.py process-all --force
python process.py export-all
python process.py export --categories spa pool
python process.py status
python process.py status -v
python process.py status -v --categories spa
python process.py retry-errors
python process.py retry-errors --categories golf
python process.py check-prompts
```

---

## 12. What Not To Do

- Do not use async, threads, or parallel API execution
- Do not modify prompt files in code
- Do not modify source template files in code
- Do not write into `pages/`
- Do not invent enum values
- Do not fill quote fields with generated text
- Do not create placeholder absence rows
- Do not use `Meeting & Events Capacity Details.xlsx`

---

## 13. Dependencies

```text
google-genai>=1.0.0
openpyxl>=3.1.0
requests>=2.31.0
```

No extra libraries without approval.
