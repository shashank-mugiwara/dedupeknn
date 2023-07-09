from req import KnnSearchV1
from req import KnnSearchVectorFields
from req import KnnSearchIndex
from req import KnnSearchQuery
from req import KnnSearchV1
from clients import LoadOpenSearchClient
from config import OpensearchConfig
import json
import rapidfuzz
from rapidfuzz import utils, process

opensearch_client = LoadOpenSearchClient.get_opensearch_client()
config = OpensearchConfig.get_config()


async def get_similar_knn(vector: list, size: int, k: int):
    knn_fields = KnnSearchVectorFields(vector=vector, k=k)
    knn_search_index = KnnSearchIndex(dedupe_vector_nmslib=knn_fields)
    knn_search_query = KnnSearchQuery(knn=knn_search_index)
    opensearch_search_query = KnnSearchV1(query=knn_search_query, size=size)

    response = await opensearch_client.search(body=json.loads(opensearch_search_query.json()),
                                              index=config['INDEX_NAME'][0])
    return response


async def address_match(input_text: str, vector: list, size: int, k: int, threshold: float):
    response = await get_similar_knn(vector=vector, k=k, size=size)
    texts = construct_similarity_response(opensearch_response=response)
    if len(texts) == 0:
        return []
    processed_texts = [utils.default_process(text) for text in texts]
    input_text = utils.default_process(input_text)
    matches = process.extract(input_text, processed_texts, limit=2,
                              scorer=rapidfuzz.fuzz.partial_ratio)

    response = {'matches': []}
    for match in matches:
        thresh = match[1]
        if thresh >= threshold:
            response['matches'].append({'text': texts[match[2]], 'match_score': match[1]})
    return response


def construct_similarity_response(opensearch_response):
    texts = []
    if 'timed_out' in opensearch_response and opensearch_response['timed_out'] == False:
        if opensearch_response['hits']['total']['value'] > 0:
            for hit in opensearch_response['hits']['hits']:
                texts.append(hit['_source']['input_string'])

    return texts
