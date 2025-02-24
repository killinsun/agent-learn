from abc import abstractmethod, ABC
from typing import Type

from pydantic import BaseModel


class ChatParams(BaseModel):
    temperature: float | None = None
    top_k: int | None = None
    seed: int | None = None
    max_tokens: int | None = None
    expected_format: Type[BaseModel] | None = None


class BaseLLM(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], params: ChatParams):
        raise NotImplementedError
