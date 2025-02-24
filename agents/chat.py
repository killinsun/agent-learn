import json
import textwrap
from pprint import pprint
from typing import Any

from openai.types.chat import ChatCompletion

from chat_history.conversation import LocalConversationHistory
from llm.base import ChatParams
from llm.openai_llm import OpenAILLM
from tools.base_tool import BaseTool


class ChatAgent:

    def __init__(
        self, tools: list[BaseTool], conversation_repo: LocalConversationHistory
    ):
        self.tools = tools
        tool_definitions = [tool.definition for tool in tools]
        tool_names = [tool.definition["function"]["name"] for tool in tools]
        self.llm = OpenAILLM(model_name="gpt-4o", tools=tool_definitions)

        self.repo = conversation_repo

        self.system_prompt = textwrap.dedent(
            f"""
        あなたはホテル＆テーマパークのアシスタントエージェントです。
        ユーザーの質問に対し、ホテルやテーマパークのことについて回答します。
        
        回答するために必要な情報があれば検索をしたり、ユーザーに質問するためのツール「{tool_names}」を使用し、そこから不足情報を補って回答します。
        必要な情報が出揃い、最終回答する時はツールは使用せずに出力します。
        会話を続ける場合は得られた情報をベースに回答していきます。
        
        ホテルの一覧 = [
            "ホテルヨーロッパ",
            "ホテルアムステルダム",
            "ホテルデンハーグ",
            "フォレストヴィラ",
            "ホテルロッテルダム"
        ]
        """
        )
        try:
            self.messages = conversation_repo.get_past_conversation()
        except FileNotFoundError:
            self.messages = [{"role": "system", "content": self.system_prompt}]

    def run(self, question: str) -> None:
        user_message = {"role": "user", "content": question}
        self.messages.append(user_message)

        return self._chat()

    def _chat(self):
        result = self.llm.chat(messages=self.messages, params=ChatParams())
        self._save_llm_response(result)

        if self._has_tool_call(result):
            self._call_tool(result)
        else:
            pprint(result.choices[0].message.content)

        self.repo.save(self.messages)

    def _save_llm_response(self, result: ChatCompletion):
        assistant_message = result.choices[0].message

        if self._has_tool_call(result):
            tool_call = assistant_message.tool_calls[0]
            message_dict = {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ],
            }
        else:
            message_dict = {
                "role": assistant_message.role,
                "content": assistant_message.content,
            }

        self.messages.append(message_dict)

    def _find_tool_from_name(self, name: str) -> BaseTool | None:
        for tool in self.tools:
            if tool.definition["function"]["name"] == name:
                return tool

        print(f"Not found tool name:{name}")
        return None

    def _has_tool_call(self, completion: ChatCompletion) -> bool:
        return completion.choices[0].message.tool_calls is not None

    def _call_tool(self, completion: ChatCompletion):
        tool_call_id = completion.choices[0].message.tool_calls[0].id
        tool_name = completion.choices[0].message.tool_calls[0].function.name
        arguments = completion.choices[0].message.tool_calls[0].function.arguments

        arguments_dict = json.loads(arguments)

        tool = self._find_tool_from_name(tool_name)
        tool_result = tool.call(**arguments_dict)

        self.messages.append(
            {
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": tool_name,
                "content": tool_result,
            }
        )

        return self._chat()
