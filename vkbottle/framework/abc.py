from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import NoReturn

from vkbottle.api import ABCAPI
from vkbottle.polling import ABCPolling


class ABCFramework(ABC):
    api: ABCAPI

    @property
    @abstractmethod
    def polling(self) -> ABCPolling:
        pass

    @property
    @abstractmethod
    def loop(self) -> AbstractEventLoop:
        pass

    @abstractmethod
    async def run_polling(self) -> NoReturn:
        pass

    @abstractmethod
    def run_forever(self) -> NoReturn:
        pass
