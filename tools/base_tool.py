from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    definition: dict

    @abstractmethod
    def call(self, **kwargs) -> str | list[dict[str, Any]]:
        pass
