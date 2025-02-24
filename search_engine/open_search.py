from opensearchpy import OpenSearch

from config import config


class FullTextSearchRetriever:

    def __init__(self, index_names: list[str], client: OpenSearch):
        self.index_names = index_names
        self.client = client

    def search(self, query: str, top_k: int = 5):
        body = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"document": {"query": query}}},
                    ],
                    "minimum_should_match": 1,
                }
            }
        }

        response = self.client.search(index=self.index_names, body=body)

        return response


def get_opensearch_client():
    opensearch_conf = config.opensearch

    hosts = [
        {"host": host, "port": opensearch_conf.port} for host in opensearch_conf.hosts
    ]

    client = _get_client_for_local(
        hosts, opensearch_conf.user, opensearch_conf.password
    )
    return client


def _get_client_for_local(hosts, user, password):
    auth = (
        user,
        password,
    )

    client = OpenSearch(
        hosts=hosts,
        http_compress=True,
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    return client
