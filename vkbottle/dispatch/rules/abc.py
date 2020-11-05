from abc import ABC, abstractmethod
from typing import Union

from vkbottle_types.events import BaseUserEvent, BaseGroupEvent


class ABCRule(ABC):
    @abstractmethod
    async def check(self, event: Union[BaseUserEvent, BaseGroupEvent]):
        pass

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"
