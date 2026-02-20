# HVAC Scraper

A FastAPI service that scrapes HVAC manufacturer websites, downloads product manuals, and saves the extracted text as structured JSON files. Built as the data pipeline for an AI-assisted manual search and diagnostic app.

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn playwright pdfplumber httpx
playwright install chromium
```


## Usage

**Option 1 — CLI (recommended for testing)**
```bash
python3 cli.py
```
Starts the server automatically and prompts you for a manufacturer and model number.

**Option 2 — API directly**
```bash
uvicorn main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"manufacturer": "carrier", "model_number": "58STA"}'
```

---

## Output

Files are saved to `output/manufacturer/json/` and `output/manufacturer/pdf/`.

---

## Adding a Manufacturer

Add a new entry to `MANUFACTURERS` in `configs.py`. No other files need to change.
