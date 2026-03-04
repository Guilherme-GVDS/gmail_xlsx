# gmail_xlsx_sync

CLI script in Python to fetch `.xlsx` attachments from Gmail by subject and append
data to a base spreadsheet.

## Current status

Initial project scaffold based on `PRD.md` and `docs/readme.md`.

## Prerequisites

- Python 3.13
- Gmail API OAuth credentials (`credentials.json`)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust values.
4. Place `credentials.json` in project root.
5. Ensure `core/base.xlsx` exists with the expected columns.

## Run

```bash
python main.py
```

