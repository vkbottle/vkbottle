from vkbottle.api import ABCAPI
from abc import ABC, abstractmethod
from vkbottle.polling import ABCPolling
from typing import NoReturn
from asyncio import AbstractEventLoop


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
