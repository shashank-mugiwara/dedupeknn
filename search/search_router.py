import io
import logging
from logging.config import dictConfig
from config import opensearch_config
from starlette import status

from search import address_match

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from resp import DocumentInsertResponse

from logger import DedupeKnnLogger
from req import OpensearchVectorDocumentV1
from clients import LoadOpenSearchClient
from fastapi import APIRouter
import json
from req import KnnSimilaritySearch, KnnSearchIndex, KnnSearchVectorFields, \
    KnnSearchV1, KnnSearchQuery

from utils.fast_text_utils import generate_sentence_vector
from search import get_similar_knn

router = APIRouter()
opensearch_client = LoadOpenSearchClient().get_opensearch_client()
config = opensearch_config.OpensearchConfig().get_config()

logger = logging.getLogger("dedupeknn")
dictConfig(DedupeKnnLogger().dict())


@router.post("/api/v1/similarity/knn/search")
async def get_similar_records_from_opensearch(req: KnnSimilaritySearch):
    logger.info("Got request for similarity match: {}".format(jsonable_encoder(req)))

    if req.text is None or req.text == "":
        return JSONResponse(content="Please give valid text.", status_code=status.HTTP_400_BAD_REQUEST)
    sentence_vector = generate_sentence_vector(req.text)
    response = await get_similar_knn(vector=sentence_vector.tolist(), k=req.k, size=req.size)
    response = construct_similarity_response(opensearch_response=response)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.post("/api/v1/similarity/address/search")
async def get_similar_records_from_opensearch(req: KnnSimilaritySearch):
    logger.info("Got request for similarity match: {}".format(jsonable_encoder(req)))

    if req.text is None or req.text == "":
        return JSONResponse(content="Please give valid text.", status_code=status.HTTP_400_BAD_REQUEST)

    sentence_vector = generate_sentence_vector(req.text)
    response = await address_match(input_text=req.text, k=req.k, size=req.size,
                                   vector=sentence_vector.tolist(), threshold=req.threshold)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


def construct_similarity_response(opensearch_response):
    successful_response = {}
    hits = []
    if 'timed_out' in opensearch_response and opensearch_response['timed_out'] == False:
        if opensearch_response['hits']['total']['value'] > 0:
            successful_response['total'] = opensearch_response['hits']['total']['value']

            for hit in opensearch_response['hits']['hits']:
                h = {'id': hit['_id'], 'text': hit['_source']['input_string'], 'score': hit['_score']}
                hits.append(h)

            successful_response['hits'] = hits
    return successful_response
