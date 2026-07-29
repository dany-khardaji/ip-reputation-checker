from fastapi import FastAPI
from check_ip import check_ip

app = FastAPI()


@app.get("/check")
def check_endpoint(ip: str):
    return check_ip(ip)