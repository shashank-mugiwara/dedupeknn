from req import KnnSearchV1
from req import KnnSearchVectorFields
from req import KnnSearchIndex
from req import KnnSearchQuery
from req import KnnSearchV1
from clients import LoadOpenSearchClient
from config import OpensearchConfig
import json

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
