from abc import ABC, abstractmethod


class BaseTool(ABC):

    definition: dict

    @abstractmethod
    def call(self, **kwargs) -> str:
        pass
