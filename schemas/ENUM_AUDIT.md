# Enum Audit — schemas/

## Status

Template Excel files were not available in `input/` at the time of this audit
(only `export-hotel.xlsx` is present). All enum `allowed_values` were inferred
from element labels, column names, or example data. Items marked `# UNVERIFIED`
in the schema files have not been confirmed against a real CMS dropdown cell.

---

## pool.py — Water Feature Type

**Fix applied:** Removed duplicate `"2. Resort Style Pool"` (no hyphen).
Retained `"2. Resort-Style Pool"` (with hyphen) as the canonical value because:
- The element label is `Resort-Style Pool` (with hyphen)
- All related column names use `Resort-Style Pool` (with hyphen)
- The `1.` value also uses `Resort-Style Pool Experience` (with hyphen)

**Remaining UNVERIFIED entries** (cannot resolve without the real template):
- `"1. Resort-Style Pool Experience"`
- `"2. Resort-Style Pool"`
- `"3. Rooftop Pool Experience"`
- `"4. Lazy River"`
- `"5. Waterpark"`

**Action required:** Open `Pool & Water Feature Form.xlsx` and check the dropdown
validation cell for the "Water Feature Type" column. Confirm numbering and exact
spelling for all five values.

---

## spa.py

### ON-SITE Only - SPA Experiences Available

Values inferred from element structure:
- `"1. No Spa On-site"` — UNVERIFIED
- `"2. Full Service Spa"` — UNVERIFIED
- `"3. Spa Services"` — UNVERIFIED
- `"4. Thermal Spa"` — UNVERIFIED

### Facilities of the Spa

Contains a likely duplicate/inconsistency:
- `"Relaxation Lounge"` and `"4. Relaxation Lounge"` — one of these is wrong.
  The numbered form `"4. Relaxation Lounge"` conflicts with the unnumbered form.
  **Action required:** check the CMS dropdown to determine which is correct, then
  remove the other. Currently both are present in `allowed_values`.

Other values: UNVERIFIED (no template available).

### Massage Therapy Options, Wellness & Holistic Therapy Options

All values: UNVERIFIED.

---

## dining.py

### Does the hotel have a on-site restuarant?

- `"Yes"` / `"No"` — plausible, but UNVERIFIED against CMS template.

### Dietary Menu Options

- `"1. Vegan"`, `"2. Vegetarian"`, `"3. Gluten Free"`, `"4. None of the above"` — UNVERIFIED.

### Meals Served

- `"1. Breakfast"`, `"2. Brunch"`, `"3. Lunch"`, `"4. Dinner"` — UNVERIFIED.

---

## meetings.py

### Meetings and Events facilities & space options

All values UNVERIFIED. Notable: `"3. Meetings and Events"`, `"3a."`, `"3b."`,
`"3c."`, `"3d."` use a sub-numbering scheme that is unusual — verify against template.

### Amenities & Services available

All values UNVERIFIED (long list, high risk of mismatch).

### Occasions ROUTINELY hosted at the hotel

All values UNVERIFIED.

---

## golf.py

### Type of Golf Experience

- `"On-site"`, `"Nearby"`, `"No golf onsite or near the hotel"` — UNVERIFIED.

### Available Facilities

Contains likely duplicate/inconsistency:
- `"Pro Shop"` and `"Pro-Shop"` — hyphenated vs. unhyphenated forms both present.
  **Action required:** verify which form the CMS uses and remove the other.
- All other values: UNVERIFIED.

---

## experiences.py

### Select each experience your hotel offers

All values UNVERIFIED. Source: element labels.

---

## Recommended next step

Place all CMS template Excel files in `input/` and re-run T-08 using openpyxl to
read dropdown validation cells. The audit function in `process.py` (`_run_column_audit`)
checks structural consistency but cannot validate enum values against CMS dropdowns.
