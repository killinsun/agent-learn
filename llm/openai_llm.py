from config import config
from openai import OpenAI

from llm.base import BaseLLM, ChatParams

client = OpenAI(api_key=config.openai_api_key)


class OpenAILLM(BaseLLM):
    def __init__(self, model_name: str = "gpt-4o", tools: list | None = None):
        self._model_name = model_name

        self._tools = tools
        self._tool_choice = None
        if self._tools:
            self._tool_choice = "auto"

    def chat(self, messages: list[dict[str, str]], params: ChatParams):
        if params.expected_format:
            chat_completion = self._chat_completion_beta(messages, params)
        else:
            chat_completion = self._chat_completion(messages, params)

        return chat_completion

    def _chat_completion(self, messages: list[dict[str, str]], params: ChatParams):
        return client.chat.completions.create(
            model=self._model_name,
            temperature=params.temperature,
            messages=messages,
            seed=params.seed,
            max_tokens=params.max_tokens,
            tools=self._tools,
            tool_choice=self._tool_choice,
        )

    def _chat_completion_beta(
        self, messages: list[dict[str, str]], params: ChatParams | None
    ):
        return client.beta.chat.completions.parse(
            model=self._model_name,
            temperature=params.temperature if params else None,
            messages=messages,
            seed=params.seed if params else None,
            max_tokens=params.max_tokens if params else None,
            response_format=(
                params.expected_format if params and params.expected_format else None
            ),
            tools=self._tools,
            tool_choice=self._tool_choice,
        )
