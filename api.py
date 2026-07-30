from fastapi import FastAPI, HTTPException
from check_ip import check_ip


app = FastAPI()

@app.get("/check")
def check_endpoint(ip: str):
    result = check_ip(ip)
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result

