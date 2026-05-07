# Hotel Info Filler

A comprehensive tool for extracting, processing, and verifying hotel information from websites. Crawls hotel sites using Firecrawl, extracts structured content (dining, spa, pool, golf, meetings, experiences) via AI models, verifies and enriches the data, and exports results to Excel. Includes a standalone tool for finding nearby golf courses via Google Places API.

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Dependencies: `pip install -r requirements.txt`

### Setup

1. **Create a `.env` file** in the project root with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   GOOGLE_PLACES_API_KEY=your_google_places_api_key
   ```

2. **Prepare input data**: Place hotel data in `input/export-hotel.xlsx`
   - Required columns: `Property ID`, `Nome account`, `Sito Web`
   - For golf proximity search: also add `fLatitude` and `fLongitude` columns

3. **Basic workflow**:
   ```bash
   # Crawl a single hotel website
   python process.py crawl 98419
   
   # Extract and process content
   python process.py process 98419
   
   # Export results to Excel
   python process.py export --categories dining spa pool
   ```

---

## CLI Commands

### Main Pipeline: `process.py`

#### Crawling

**`crawl <property-id>`** — Crawl a single hotel website via Firecrawl
```bash
python process.py crawl 98419
python process.py crawl 98419 --depth 2 --limit 20
```
- `--depth <N>` — Maximum crawl depth (default: 3)
- `--limit <N>` — Maximum pages to crawl (default: 50)

**`crawl-all`** — Crawl all hotels with a website
```bash
python process.py crawl-all
python process.py crawl-all --depth 2 --limit 20
```

#### Processing

**`process <property-id>`** — Extract and process content from a single hotel
```bash
python process.py process 98419
python process.py process 98419 --categories dining spa
python process.py process 98419 --categories pool --force
```
- `--categories <cat1 cat2 ...>` — Which categories to process (default: all)
- `--force` — Reprocess even if already done

**`process-all`** — Process all hotels
```bash
python process.py process-all
python process.py process-all --categories golf meetings --force
```

#### Export

**`export --categories <cat1 cat2 ...>`** — Export specific categories to Excel
```bash
python process.py export --categories dining spa
python process.py export --categories pool
```

**`export-all`** — Export all categories
```bash
python process.py export-all
```

Outputs files like: `output/dining-extracted.xlsx`, `output/pool-verified.xlsx`, `output/spa-editorial.xlsx`

#### Status & Maintenance

**`status`** — Show processing status for all hotels
```bash
python process.py status
python process.py status --verbose
python process.py status --categories pool
```
- `-v, --verbose` — Show detailed status per hotel
- `--categories <cat1 cat2 ...>` — Filter by categories

**`retry-errors`** — Reprocess hotels that previously failed
```bash
python process.py retry-errors
python process.py retry-errors --categories pool spa
```

**`check-prompts`** — Verify all prompts are configured
```bash
python process.py check-prompts
```

---

### Golf Proximity Search: `golf_proximity.py`

Standalone tool to find golf clubs within 16 km of each hotel using Google Places API.

**Setup**: Add `fLatitude` and `fLongitude` columns to `input/export-hotel.xlsx` with coordinates in Italian thousands-separator format (e.g., `43.781.410`).

**`golf_proximity.py`** — Find golf clubs for all hotels with coordinates
```bash
python golf_proximity.py
```

**`--property-id <id>`** — Process a single hotel
```bash
python golf_proximity.py --property-id 98419
```

**`--output <path>`** — Custom output file path
```bash
python golf_proximity.py --output results.xlsx
```

Output: `output/golf-proximity-YYYY-MM-DD.xlsx`
- One row per golf club found
- Columns: Property ID, Hotel Name, Latitude, Longitude, Golf Club Name, Distance (km), Address, Website
- Hotels with no clubs get one row with empty club fields

---

## Categories

Available content categories for extraction:

| Category | Description |
|---|---|
| `dining` | Restaurants, bars, dining options, menus |
| `spa` | Spa facilities, wellness services, massages, thermal treatments |
| `pool` | Swimming pools, water features, aqua parks |
| `golf` | Golf courses, golf amenities |
| `meetings` | Conference facilities, event spaces, banquet halls |
| `experiences` | Entertainment, activities, attractions, entertainment venues |

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Google API key for Places API and Geolocation | Yes |
| `OPENROUTER_API_KEY` | OpenRouter API key for model inference | Yes |
| `FIRECRAWL_API_KEY` | Firecrawl API key for web crawling | Yes |
| `GOOGLE_PLACES_API_KEY` | Google Places API key for golf proximity search | For golf_proximity.py only |

---

## Project Structure

```
hotel-info-filler_NEW/
├── input/
│   └── export-hotel.xlsx              # Input: hotel data with website URLs
├── output/
│   ├── checkpoint-*.json              # Processing checkpoints (state tracking)
│   ├── *-extracted.xlsx               # Raw extracted content per category
│   ├── *-verified.xlsx                # Verified (cleaned/validated) content
│   ├── *-editorial.xlsx               # Final with editorial enrichment
│   └── golf-proximity-*.xlsx          # Golf proximity search results
├── pages/                             # Cached crawled HTML pages
├── prompts/                           # AI prompts for extraction and writing
│   ├── presence_detection.txt
│   ├── *_extraction.txt               # Category-specific extraction prompts
│   └── *_writer.txt                   # Category-specific editorial writing prompts
├── schemas/                           # Data schemas (field definitions)
├── core/                              # Core modules
│   ├── checkpoint.py                  # State management
│   ├── context.py                     # Context preparation for models
│   ├── exporter.py                    # Excel export
│   ├── extractor.py                   # Content extraction via AI
│   ├── logger.py                      # Logging utilities
│   ├── verifier.py                    # Data verification
│   └── writer.py                      # Editorial content generation
├── process.py                         # Main CLI entry point
├── golf_proximity.py                  # Golf proximity search (standalone)
├── config.py                          # Configuration and constants
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## Examples

### Single hotel full pipeline

```bash
# 1. Crawl the website
python process.py crawl 98419 --depth 3

# 2. Process all categories
python process.py process 98419

# 3. Export specific categories
python process.py export --categories dining spa pool

# 4. Check status
python process.py status --verbose
```

### Batch processing

```bash
# Crawl all hotels
python process.py crawl-all --depth 2 --limit 20

# Process all hotels for specific categories
python process.py process-all --categories dining golf

# Force reprocessing
python process.py process-all --force

# Export all
python process.py export-all
```

### Golf proximity search

```bash
# All hotels with coordinates
python golf_proximity.py

# Single hotel
python golf_proximity.py --property-id 98419

# Custom output
python golf_proximity.py --output golf_results.xlsx
```

### Maintenance

```bash
# Check configuration
python process.py check-prompts

# View processing status
python process.py status

# Reprocess failed hotels
python process.py retry-errors --categories pool

# Reprocess specific category for all hotels
python process.py process-all --categories spa --force
```

---

## Configuration

Key settings are in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `GEMINI_MODEL` | `gemini-flash-latest` | Model for extraction |
| `OPENROUTER_MODEL` | `openai/gpt-4o` | Model for editorial writing |
| `GEMINI_TEMPERATURE` | 0.1 | Extraction model temperature |
| `WRITER_TEMPERATURE` | 0.4 | Editorial writing model temperature |
| `GEMINI_MAX_TOKENS` | 8192 | Extraction response limit |
| `WRITER_MAX_TOKENS` | 4096 | Editorial response limit |
| `FIRECRAWL_MAX_DEPTH` | 3 | Default crawl depth |
| `FIRECRAWL_PAGE_LIMIT` | 50 | Default pages to crawl |
| `MIN_CATEGORY_CHARS` | 300 | Minimum content length to consider presence |
| `VERIFIER_RETRY_MAX` | 3 | Retry attempts for extraction |
| `WRITER_RETRY_MAX` | 3 | Retry attempts for editorial writing |

---

## Troubleshooting

### Missing API key error
```
Error: Missing required environment variables: GOOGLE_API_KEY, ...
```
**Solution**: Ensure `.env` file exists in the project root with all required keys:
```
KEY_NAME=your_value
```
No quotes needed. Keys should not have spaces around the `=` sign.

### Firecrawl crawl fails
```
Crawl error: timeout or connection refused
```
**Solutions**:
- Verify `FIRECRAWL_API_KEY` is valid
- Check that the hotel website URL in `input/export-hotel.xlsx` is reachable
- Reduce `--depth` and `--limit` to avoid timeouts
- Add delays by increasing `REQUEST_DELAY` in `config.py`

### JSON parse error during extraction
```
Invalid JSON returned by model: Expecting ',' delimiter...
```
**Solutions**:
- This indicates the model returned malformed JSON; automatic retries will occur
- If it persists, check the `GEMINI_MAX_TOKENS` setting in `config.py`
- Ensure extraction prompts include the "omit null fields" instruction

### Golf proximity: no results found
```
No hotels with coordinates found.
Add 'fLatitude' and 'fLongitude' columns to input/export-hotel.xlsx and retry.
```
**Solutions**:
- Add `fLatitude` and `fLongitude` columns to `input/export-hotel.xlsx`
- Ensure coordinates are properly formatted (Italian thousands-separator: `43.781.410`)
- Verify `GOOGLE_PLACES_API_KEY` is set in `.env` and is valid
- Check that golf clubs exist near the hotel location

### No pages crawled
```
Crawl successful but 0 pages found
```
**Solutions**:
- Verify the hotel website URL is correct and publicly accessible
- Check if the website blocks automated crawlers
- Try increasing `--limit` to allow more pages
- Check Firecrawl API status for any service issues

### Export file not created
```
No data to export for category 'dining'
```
**Solutions**:
- First run `python process.py process <property-id> --categories dining`
- Check status: `python process.py status --verbose`
- Verify the checkpoint file exists: `output/checkpoint-dining.json`

---

## Data Flow

```
input/export-hotel.xlsx
    ↓
[crawl-all] → pages/*
    ↓
[process-all] → checkpoint-*.json (state tracking)
    ↓
[extract] → raw extraction via AI models
    ↓
[verify] → data validation and normalization
    ↓
[write] → editorial enrichment
    ↓
[export] → output/*-extracted.xlsx, *-verified.xlsx, *-editorial.xlsx
```

---

## Performance Notes

- Each hotel crawl: 10–30 seconds (depends on site size and `--depth`)
- Each category extraction: 20–60 seconds (AI model call)
- Full pipeline (crawl + process + export): 2–5 minutes per hotel
- Batch processing saves time on export by consolidating multiple hotels
- Golf proximity search: 1–2 seconds per hotel (Google Places API)

---

## Support

For issues, error logs are stored in the processing checkpoints and console output. Use `--verbose` flags to get more details on processing steps.

Common log locations:
- Process logs: console output with [STEP X] markers
- Checkpoints: `output/checkpoint-*.json` with detailed state
- Status: `python process.py status --verbose` for all hotels
