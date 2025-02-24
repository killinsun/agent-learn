from tools.base_tool import BaseTool


class AskUserTool(BaseTool):
    definition = {
        "type": "function",
        "function": {
            "name": "ask_user",
            "description": "回答に必要な情報が揃っていない場合に、ユーザーに対して逆質問することで、情報の絞り込みを行います",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "ユーザーへの質問",
                    },
                    "options": {
                        "type": "array",
                        "description": "もしユーザーにクローズドクエスチョンをしたい場合の回答一覧。オープンクエスチョンの場合は空にする",
                        "items": {"type": "string"},
                    },
                },
            },
        },
    }

    def call(self, **kwargs) -> str:
        question = kwargs.get("question")
        options = kwargs.get("options", [])

        print(
            f"エージェントはAskUserTool を選択しました。 質問: {question}, options: {options}"
        )

        if len(options) >= 1:
            for index, option in enumerate(options):
                print(f"{index + 1}. {option}")

            choice = input("(数字を入力) >")
            if choice not in [str(i) for i in range(1, len(options) + 1)]:
                print("正しい選択肢を選んでください")
                return self.call(**kwargs)

            return options[int(choice) - 1]

        user_input = input(">")
        return user_input
