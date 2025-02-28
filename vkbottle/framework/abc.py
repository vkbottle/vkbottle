from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.polling import ABCPolling


class ABCFramework(ABC):
    api: "ABCAPI"

    @property
    @abstractmethod
    def polling(self) -> "ABCPolling": ...

    @abstractmethod
    async def run_polling(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def run_forever(self) -> NoReturn:
        raise NotImplementedError


__all__ = ("ABCFramework",)
