import io
import logging
from logging.config import dictConfig
from logger import DedupeKnnLogger
from models import OpensearchVectorDocumentV1

from fastapi import APIRouter, UploadFile, File, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import FileResponse, JSONResponse, StreamingResponse

router = APIRouter()

logger = logging.getLogger("dedupeknn")
dictConfig(DedupeKnnLogger().dict())


@router.post("/api/v1/knn/doc/insert")
async def ingest_document(document: OpensearchVectorDocumentV1):
    return "OK"

