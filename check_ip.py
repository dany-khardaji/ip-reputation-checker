"""ip-reputation-checker — Networking/APIs phase, main project.

Build this ONE STEP AT A TIME. Do not fill in everything at once.
Right now this file is at STEP 1: just confirm your tools are installed and
your imports work. The real request comes in Step 2 — don't write it yet.

Run this file. If it prints the success line with no ImportError, Step 1 is done.
"""

import requests          # the HTTP tool you'll use to call the API
# You'll also need something to load your API key from a .env file later.
# Leave that import out for now — we add it at Step 5, when you actually
# move the key out of the code. One tool at a time.


def main():
    # STEP 1 ONLY: prove the imports work. That's it.
    print("Imports OK. requests version:", requests.__version__)

    # --- STOP HERE. ---
    # Step 2 (next): make a GET request to the AbuseIPDB /check endpoint
    # with a HARDCODED test IP (118.25.6.39), and print:
    #     response.status_code
    #     response.text
    # You'll need three things for that request, and Claude will walk you
    # through them one at a time when you're ready:
    #   - the URL
    #   - headers (your API key + Accept)
    #   - params (the ipAddress and maxAgeInDays)
    # Do NOT write Step 2 yet. Get Step 1 running first.


if __name__ == "__main__":
    main()
