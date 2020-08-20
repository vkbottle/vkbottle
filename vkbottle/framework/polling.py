from abc import ABC, abstractmethod
from vkbottle.http import HTTP
import typing
import asyncio

if typing.TYPE_CHECKING:
    from .bot.bot import AnyBot, Api
    from .user.user import AnyUser, UserApi


class PollingAPI(ABC, HTTP):
    long_poll_server: dict
    wait: int
    version: int = None

    @staticmethod
    @abstractmethod
    def get_id_by_token(token: str, loop: asyncio.AbstractEventLoop) -> int:
        pass

    @abstractmethod
    def dispatch(self, *instance: typing.Union["AnyBot", "AnyUser"]) -> None:
        pass

    @abstractmethod
    def get_server(self) -> dict:
        pass

    @abstractmethod
    def make_long_request(self, long_poll_server: dict) -> dict:
        pass

    @abstractmethod
    async def run(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def run_polling(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def api(self) -> typing.Union["Api", "UserApi"]:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
