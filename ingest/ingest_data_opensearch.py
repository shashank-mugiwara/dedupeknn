import io
import logging
from logging.config import dictConfig
from logger import DedupeKnnLogger
from models import OpensearchVectorDocumentV1
from clients import LoadOpenSearchClient
from fastapi import APIRouter

router = APIRouter()
opensearch_client = LoadOpenSearchClient().get_opensearch_client()

logger = logging.getLogger("dedupeknn")
dictConfig(DedupeKnnLogger().dict())


@router.post("/api/v1/knn/doc/insert")
async def ingest_document(document: OpensearchVectorDocumentV1):
    return opensearch_client is None

