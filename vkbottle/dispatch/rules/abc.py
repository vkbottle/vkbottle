from abc import ABC, abstractmethod
from vkbottle_types.events import BaseUserEvent, BaseGroupEvent
from typing import Union


class ABCRule(ABC):
    @abstractmethod
    async def check(self, event: Union[BaseUserEvent, BaseGroupEvent]):
        pass

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"
