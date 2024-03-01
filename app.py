from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import requests
import os
import uvicorn
from pydantic import BaseModel
from typing import Literal

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

class SendRequestModel(BaseModel):
    method: Literal["get", "post", "put", "delete"]
    url: str
    json: dict = None
    headers: dict = None
    cookies: dict = None

@app.post("/send_request")
def send_request(
    data: SendRequestModel
):
    try:
        method = getattr(requests, data.method)
        response = method(
            url=data.url,
            json=data.json,
            headers=data.headers,
            cookies=data.cookies
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail={
            "error": "RequestException",
            "message": str(e)
        
        }) 

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