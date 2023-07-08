import io
import logging
from logging.config import dictConfig
from config import opensearch_config
from starlette import status

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from resp import DocumentInsertResponse

from logger import DedupeKnnLogger
from req import OpensearchVectorDocumentV1
from clients import LoadOpenSearchClient
from fastapi import APIRouter
import json

from utils.fast_text_utils import generate_sentence_vector

router = APIRouter()
opensearch_client = LoadOpenSearchClient().get_opensearch_client()
config = opensearch_config.OpensearchConfig().get_config()

logger = logging.getLogger("dedupeknn")
dictConfig(DedupeKnnLogger().dict())


@router.post("/api/v1/knn/doc/insert")
async def ingest_document(document: OpensearchVectorDocumentV1):
    logger.info('Received request: {}'.format(jsonable_encoder(document)))
    sentence_vector = generate_sentence_vector(document.text)
    document = {
        "dedupe_vector_nmslib": sentence_vector,
        "input_string": document.text
    }
    response = await opensearch_client.index(
        index=config['INDEX_NAME'][0],
        body=document,
        refresh=True
    )

    if response is not None and response['result'] is not None:
        if response['result'] == 'created':
            rp = DocumentInsertResponse()
            rp.success = True
            rp.seq_no = response['_seq_no']
            return JSONResponse(content=json.loads(rp.json()), status_code=status.HTTP_200_OK)

    rp = DocumentInsertResponse()
    rp.success = False
    rp.seq_no = 0
    return JSONResponse(content=json.loads(rp.json()), status_code=status.HTTP_400_BAD_REQUEST)
