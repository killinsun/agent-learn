import textwrap
from pprint import pprint

from search_engine.open_search import FullTextSearchRetriever
from tools.base_tool import BaseTool


class SearchDocsTool(BaseTool):
    retriever: FullTextSearchRetriever

    definition = {
        "type": "function",
        "function": {
            "name": "search_relevant_docs",
            "description": "キーワードから関連ドキュメントを検索します",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "検索キーワード。単語もしくは自然言語での入力",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "何件分取得するかどうか",
                    },
                },
            },
        },
    }

    def __init__(self, retriever: FullTextSearchRetriever):
        self.retriever = retriever

    def call(self, **kwargs):
        query = kwargs.get("query")
        top_k = kwargs.get("top_k", 5)

        print(
            textwrap.dedent(
                f"""
                エージェントはSearchDocsTool を選択しました。 
                検索キーワード: {query}, top_k: {top_k}"""
            )
        )

        got = self.retriever.search(query, top_k)

        print(f"{len(got)} 件の検索結果が見つかりました")

        search_result = ""
        for hit in got["hits"]["hits"]:
            search_result += f"{hit['_source']['document']}\n"

        return search_result
