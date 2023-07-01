from opensearchpy import OpenSearch
from config import OpensearchConfig

config = OpensearchConfig().get_config()


class LoadOpenSearchClient:
    _client = None

    @staticmethod
    def get_opensearch_client():
        if LoadOpenSearchClient._client is None:
            client = OpenSearch(
                hosts=[{'host': config['OPENSEARCH_HOST'][0], 'port': config['OPENSEARCH_PORT'][0]}],
                http_compress=True,
                http_auth=(config['OPENSEARCH_AUTH_USERNAME'][0], config['OPENSEARCH_AUTH_PASSWORD'][0]),
                use_ssl=True,
                verify_certs=False,
                ssl_assert_hostname=True,
                ssl_show_warn=False,
            )
            LoadOpenSearchClient._client = client
            return client

