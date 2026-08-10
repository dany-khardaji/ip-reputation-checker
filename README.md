# ip-reputation-checker
**Version 1.0** Command-line tool and web API that checks whether an IP address has a
history of malicious activity, using the AbuseIPDB threat-intelligence API. Stores
every check so you can see how an IP's reputation changes over time.

## Why I built it
This is the reputation-checking module for a larger attack surface monitor I'm building. I also
used it to learn how to consume an external API and persist results with SQLite.

## What it does
- Checks an IP against AbuseIPDB and returns a verdict: BLOCK, MONITOR, or OK
- Works two ways: as a CLI tool, or as a web API
- Saves every API check to a local SQLite database
- Flags when an IP's score or verdict has changed since the last check

## Setup
1. Make sure you have Python3 installed.
2. Create and activate a virtual environment:
```bash
   python3 -m venv .venv
   source .venv/bin/activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Get a free API key at abuseipdb.com, then copy .env.example to .env and paste
   your key in.
5. Create the database:
```bash
   python3 db.py
```

## Usage
CLI:
```bash
python3 check_ip.py 8.8.8.8
```
Web API:
```bash
uvicorn api:app --reload
```
Then visit http://127.0.0.1:8000/docs for interactive docs.

## Endpoints
GET /check?ip=8.8.8.8
   Returns the current reputation. Saves the result to the database.
```json
{
  "ip": "8.8.8.8",
  "verdict": "OK",
  "score": 0,
  "country": "US",
  "isp": "Google LLC",
  "total_reports": 176
}
```
GET /history/8.8.8.8
   Returns every past check for that IP, newest first, plus change detection.
```json
{
  "ip": "8.8.8.8",
  "count": 3,
  "score_changed": false,
  "verdict_changed": false,
  "history": [
    {
      "id": 4,
      "ip": "8.8.8.8",
      "verdict": "OK",
      "score": 0,
      "country": "US",
      "isp": "Google LLC",
      "total_reports": 177,
      "checked_at": "2026-08-06 16:19:27"
    },
    {
      "id": 3,
      "ip": "8.8.8.8",
      "verdict": "OK",
      "score": 0,
      "country": "US",
      "isp": "Google LLC",
      "total_reports": 176,
      "checked_at": "2026-08-06 13:42:52"
    }
  ]
}
```

## How it works
Three files, each with one job:
- check_ip.py  - the engine. Calls AbuseIPDB, returns a dict. Never prints or saves.
- db.py        - storage. Creates the table, saves checks, reads history back.
- api.py       - the web interface. Handles HTTP, calls the other two.

The engine returns a dict and never prints or saves anything, so it doesn't care what is calling it. The CLI and the API both use the same function without either one needing its own copy of the logic. When I added the database later, I didn't have to change check_ip.py at all.

## Design decisions
- Verdict thresholds are 75 for BLOCK and 25 for MONITOR. Designed to need high confidence before blocking, as well as low scores could be noise.
- Saving happens in api.py, not inside check_ip(). The engine shouldn't know or care how it's being called. Deciding whether to save a result is a job for whoever's calling it, not for check_ip() itself.
- An IP with no history returns 200 with an empty list, not a 404. Nothing failed so it isn't an error, just no history being returned.
- Change detection returns null, not false, when there are fewer than two records. Null means not enough data to know which is the most honest.
- API errors return 502, not 200. Upstream service failed and not caller's fault. Would be misleading to return a successful 200 status code.

## Known limitations
- Only checks one source (AbuseIPDB). A single source can miss things.
- SQLite is local only. Not suitable for a deployed multi-user version.
- Free tier is capped at 1,000 checks per day.

## Built with
- Python3
- requests - HTTP calls to AbuseIPDB
- python-dotenv - keeps the API key out of the code
- FastAPI + uvicorn - the web API layer
- sqlite3 - local storage (standard library)
- argparse - CLI arguments (standard library)