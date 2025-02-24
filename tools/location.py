import random
import textwrap

from tools.base_tool import BaseTool


class LocationTool(BaseTool):
    definition = {
        "type": "function",
        "function": {
            "name": "get_location",
            "description": "ユーザーの場所情報から最寄りのホテルやパーク名を取得します",
        },
    }

    def call(self, **kwargs) -> str:
        print(textwrap.dedent(f"""エージェントはLocationTool を選択しました。"""))

        available_locations = [
            "ホテルヨーロッパ",
            "ホテルアムステルダム",
            "ホテルデンハーグ",
            "フォレストヴィラ",
            "ホテルロッテルダム",
            "ウェルカムエリア",
            "アドベンチャーパーク",
            "アトラクションタウン",
            "アートガーデン",
            "光のファンタジアシティ",
            "アムステルダムシティ" "タワーシティ",
            "ハーバータウン" "パレスハウステンボス" "入場ゲート",
        ]

        picked = self._randomly_pick(available_locations)

        print(f"ユーザーの現在位置: {picked}")

        return f"ユーザーの現在位置: {picked}"

    def _randomly_pick(self, available_locations) -> str:
        return random.choice(available_locations)
