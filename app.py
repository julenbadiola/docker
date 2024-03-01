from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import requests
import os
import uvicorn

TEST_DNS = os.environ.get('TEST_DNS', '')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 80)

app = FastAPI(
    title="Test App",
    description="This is a test app",
    version="0.0.1",
    docs_url="/",
    redoc_url=None
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/dns_test")
def dns_test():
    try:
        response = requests.get(TEST_DNS)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to TEST_DNS {TEST_DNS}") 

@app.get("/request_context")
def request_context(request: Request):
    return {
        "headers": request.headers,
        "ip": request.client.host,
    }

@app.get("/error")
def error_healthcheck():
    raise HTTPException(status_code=500, detail="Error")

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)