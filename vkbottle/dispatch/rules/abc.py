from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCRule(ABC):
    config: dict = {}

    @classmethod
    def with_config(cls, config: dict) -> Type["ABCRule"]:
        cls.config = config
        return cls

    @abstractmethod
    async def check(self, event: "Event"):
        pass

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"
