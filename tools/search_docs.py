from tools.base_tool import BaseTool


class SearchDocsTool(BaseTool):
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

    def call(self, **kwargs):
        query = kwargs.get("query")
        top_k = kwargs.get("top_k", 5)

        print(f"Search docs for {query} with top_k={top_k}")
        return f"Search docs for {query} with top_k={top_k}"
