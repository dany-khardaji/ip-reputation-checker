from fastapi import FastAPI, HTTPException  # HTTPException lets me return real error status codes
from check_ip import check_ip               # The engine, calls AbuseIPDB and returns a dict
from db import save_check                   # Storage layer, writes that dict into checks.db


app = FastAPI()


# Handles GET /check?ip=... Runs the lookup, saves it, returns JSON.
# Saving happens here and not in check_ip() so the CLI stays stateless.
@app.get("/check")
def check_endpoint(ip: str):
    result = check_ip(ip)                   # dict comes back from check_ip.py

    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])    # errors get a 502, not a misleading 200 with the error buried in the body

    save_check(result)                      # passes that same dict to db.py, saved as one row

    return result                           # FastAPI turns the dict into JSON for the browser

