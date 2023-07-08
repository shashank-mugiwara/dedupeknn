from fastapi import FastAPI, Depends, HTTPException
import uvicorn

from ingest import ingest_data_router
from utils import utils_router


app = FastAPI()
app.include_router(ingest_data_router)
app.include_router(utils_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, workers=2)
