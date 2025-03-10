import textwrap

from tools.base_tool import BaseTool
import json


class UserDefinedTool(BaseTool):
    """
    ユーザーが自由に定義したツールを呼び出せるようにしたクラス
    `definition` と `function` を渡せるようにしている。

    実際には `definition` は JSON でどこかに保存しておき、
    `function` はあらかじめ定義した関数（たとえば外部APIを叩くだけの関数など）を渡す

    LLM には str 型で返す必要があるため、関数の返り値を str に変換して返すようにしている
    """

    def __init__(self, definition: dict, function: callable):
        self.definition = definition
        self.function = function

    def call(self, **kwargs) -> str:
        return self.function(**kwargs)


def get_available_tickets() -> str:
    available_tickets = [
        {
            "ticket_name": "ネイビー",
            "price": 1000,
            "quantity": 10,
        },
        {
            "ticket_name": "キッズ",
            "price": 500,
            "quantity": 1,
        },
        {
            "ticket_name": "ゴールド",
            "price": 10000,
            "quantity": 100,
        },
        {
            "ticket_name": "バーガンディー",
            "price": 3000,
            "quantity": 5,
        },
    ]

    print(
        textwrap.dedent(
            f"""
    エージェントはget_available_tickets を選択しました。
    利用可能なチケットを取得します。
    
    以下のチケットが利用可能です:
    {available_tickets}
    
    """
        )
    )

    return json.dumps(available_tickets)


def book_ticket(ticket_type: str, quantity: int) -> str:
    print(
        textwrap.dedent(
            f"""
    エージェントはbook_ticket を選択しました。
    チケットの予約をします。
    
    予約情報:
    チケットの種類: {ticket_type}
    枚数: {quantity}
    
    """
        )
    )

    available_tickets = [
        {
            "ticket_name": "ネイビー",
            "price": 1000,
            "quantity": 10,
        },
        {
            "ticket_name": "キッズ",
            "price": 500,
            "quantity": 1,
        },
        {
            "ticket_name": "ゴールド",
            "price": 10000,
            "quantity": 100,
        },
        {
            "ticket_name": "バーガンディー",
            "price": 3000,
            "quantity": 5,
        },
    ]

    for ticket in available_tickets:
        if ticket["ticket_name"] == ticket_type:
            if ticket["quantity"] < quantity:
                return f"{ticket_type} の在庫が足りません"
            else:
                ticket["quantity"] -= quantity
                break

    return f"{quantity}枚の{ticket_type}を予約しました"


book_ticket_tool = UserDefinedTool(
    definition={
        "type": "function",
        "function": {
            "name": "book_ticket",
            "description": "チケットを予約します",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_type": {
                        "type": "string",
                        "description": "チケットの種類",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "チケットの枚数",
                    },
                },
            },
        },
    },
    function=book_ticket,
)

get_available_tickets_tool = UserDefinedTool(
    definition={
        "type": "function",
        "function": {
            "name": "get_available_tickets",
            "description": "利用可能なチケットを取得します",
            "parameters": {},
        },
    },
    function=get_available_tickets,
)
