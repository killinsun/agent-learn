import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class LocalConversationHistory:

    def __init__(self, conversation_id: str | None = "001"):
        self.conversation_id = conversation_id

    def get_past_conversation(self) -> list[dict[str, str]]:
        conversation_path = os.path.join(
            CURRENT_DIR, f"chat_{self.conversation_id}.json"
        )
        # なかったらエラーにする
        if not os.path.exists(conversation_path):
            raise FileNotFoundError("指定した履歴はありません")

        with open(conversation_path, "r") as f:
            return json.load(f)

    def save(self, messages: list[dict[str, str]]) -> None:
        conversation_path = os.path.join(
            CURRENT_DIR, f"chat_{self.conversation_id}.json"
        )
        with open(conversation_path, "w") as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)
