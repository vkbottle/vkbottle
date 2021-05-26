from abc import ABC, abstractmethod
from typing import Type, Union

from vkbottle_types.events import BaseGroupEvent, BaseUserEvent


class ABCRule(ABC):
    config: dict = {}

    @classmethod
    def with_config(cls, config: dict) -> Type["ABCRule"]:
        cls.config = config
        return cls

    @abstractmethod
    async def check(self, event: Union[BaseUserEvent, BaseGroupEvent]):
        pass

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"
