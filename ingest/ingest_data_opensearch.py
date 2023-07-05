import io
import logging
from logging.config import dictConfig

from fastapi.encoders import jsonable_encoder

from logger import DedupeKnnLogger
from req import OpensearchVectorDocumentV1
from clients import LoadOpenSearchClient
from fastapi import APIRouter
import json

router = APIRouter()
opensearch_client = LoadOpenSearchClient().get_opensearch_client()

logger = logging.getLogger("dedupeknn")
dictConfig(DedupeKnnLogger().dict())


@router.post("/api/v1/knn/doc/insert")
async def ingest_document(document: OpensearchVectorDocumentV1):
    logger.info('Received request: {}'.format(jsonable_encoder(document)))
    return "OK"