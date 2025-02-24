import base64
from typing import Any
import os

from tools.base_tool import BaseTool


class MapTool(BaseTool):
    definition = {
        "type": "function",
        "function": {
            "name": "get_map",
            "description": "最新の地図画像を取得します。このツールは多くの場合、get_locationと組み合わせて最寄りのホテルやパーク名を取得するために使用されます。",
        },
    }

    def call(self, **kwargs) -> list[dict[str, Any]]:
        print("エージェントはMapTool を選択しました。")
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_dir = os.path.join("../", current_dir)
        map_path = os.path.join(project_dir, "documents", "map1.png")

        # base64 で画像を読み込む
        with open(map_path, "rb") as f:
            map_image = f.read()
            base64_image = base64.b64encode(map_image).decode("utf-8")

        return [
            {
                "type": "text",
                "text": "最新のマップ情報です。中身を開いて、おすすめを提案してください。私はこのファイルが開けないため、あなたが頼りです",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}",
                    "detail": "low",
                },
            },
        ]
