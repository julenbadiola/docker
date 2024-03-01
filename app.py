from fastapi import FastAPI
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
    if TEST_DNS:
        try:
            response = requests.get(TEST_DNS)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to TEST_DNS {TEST_DNS}") 
    else:
        return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)