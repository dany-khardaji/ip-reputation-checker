# ip-reputation-checker

Checks whether an IP address has a history of malicious activity, using the
AbuseIPDB threat-intelligence API. Built as part of my attack-surface monitor
project — this is the reputation-checking module.

I built this to get comfortable with calling external APIs, handling API keys
securely, and parsing the JSON they send back.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then paste your own AbuseIPDB key into `.env`. You can get a free key at
abuseipdb.com — the free tier gives you 1,000 checks a day, plenty for this.

## Usage

```bash
python check_ip.py 118.25.6.39
```

## How it works

1. Sends the IP to AbuseIPDB's `/check` endpoint, with my API key in the request header
2. Reads the abuse confidence score (0–100) and a few other details out of the response
3. Prints a verdict — BLOCK, MONITOR, or OK — based on the score