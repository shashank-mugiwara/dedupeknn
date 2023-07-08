import io
import logging
from logging.config import dictConfig
from config import opensearch_config
from starlette import status

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from resp import BadRequestResponse

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


@router.post("/api/v1/vector/representation")
async def get_vector_for_sentence(document: OpensearchVectorDocumentV1):
    logger.info('Received request: {}'.format(jsonable_encoder(document)))
    sentence_vector = generate_sentence_vector(document.text)
    if sentence_vector is not None:
        return JSONResponse(content=sentence_vector.tolist(), status_code=status.HTTP_200_OK)

    bad_request_resp = BadRequestResponse(message='Unable to generate vector for the given sentence')
    return JSONResponse(content=json.dumps(bad_request_resp.json()), status_code=status.HTTP_200_OK)