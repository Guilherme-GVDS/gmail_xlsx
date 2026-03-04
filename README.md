# gmail_xlsx_sync

CLI script in Python to fetch `.xlsx` attachments from Gmail by subject and append
data to a base spreadsheet.

## Prerequisites

- Python 3.13
- Google account with Gmail enabled
- Access to Google Cloud Console

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create OAuth2 credentials in Google Cloud Console:
   - Create a project (or select an existing one).
   - Enable **Gmail API**.
   - Configure OAuth consent screen.
   - Create OAuth Client ID as **Desktop app**.
   - Download credentials and save as `credentials.json` in project root.
     (or set `GOOGLE_CREDENTIALS_PATH` in `.env`).
4. Copy `.env.example` to `.env` and set values:

```dotenv
ASSUNTO=Relatorio Financeiro Mensal
BASE_SPREADSHEET_PATH=core/base.xlsx
DOWNLOADS_DIR=downloads
PROCESSED_IDS_FILE=processed_ids.txt
KEEP_DOWNLOADS=true
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_TOKEN_PATH=token.json
```

5. Ensure `core/base.xlsx` exists with the expected output columns.
6. Run `python main.py` once to complete OAuth in the browser and generate
   `token.json`. Next runs reuse this token.

## Run

```bash
python main.py
```

## Schedule (cron)

To run every day at 08:00:

```bash
0 8 * * * cd /path/to/gmail_xlsx && /path/to/python main.py >> logs/cron.log 2>&1
```
