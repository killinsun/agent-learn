import os
import json

from opensearchpy import OpenSearch, helpers


class IndexDocsUseCase:

    def __init__(self, client: OpenSearch):
        self.client = client

    def index(self, index_name: str, docs: list[dict]):
        self._create_opensearch_index_if_not_exist(index_name, SCHEMA_CONF)

        docs_to_index = []
        for doc in docs:
            docs_to_index.append(
                {
                    "_index": index_name,
                    "_id": doc["id"],
                    "document": doc["document"],
                }
            )

        helpers.bulk(self.client, docs_to_index)

    def index_from_json_file(self, index_name: str, file_path: str):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_dir = os.path.join("../", current_dir)

        full_path = os.path.join(project_dir, file_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")

        with open(full_path, "r") as f:
            docs = json.load(f)

            self.index(index_name, docs)

        return f"Indexed {len(docs)} documents to {index_name}"

    def _create_opensearch_index_if_not_exist(self, index_name: str, schema: dict):
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=schema)


SCHEMA_CONF = {
    "settings": {
        "number_of_shards": 1,
        "analysis": {
            "filter": {
                "kuromoji_baseform_filter": {"type": "kuromoji_baseform"},
                "cjk_width_filter": {"type": "cjk_width"},
                "ja_stop_filter": {"type": "stop", "stopwords": "_japanese_"},
                "kuromoji_stemmer_filter": {"type": "kuromoji_stemmer"},
                "lowercase_filter": {"type": "lowercase"},
            },
            "analyzer": {
                "kuromoji_analyzer": {
                    "type": "custom",
                    "tokenizer": "kuromoji_tokenizer",
                    "filter": [
                        "kuromoji_baseform_filter",
                        "cjk_width_filter",
                        "ja_stop_filter",
                        "kuromoji_stemmer_filter",
                        "lowercase_filter",
                    ],
                }
            },
        },
    },
    "mappings": {
        "properties": {
            "document": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            }
        }
    },
}
