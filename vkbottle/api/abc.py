import typing
from abc import ABC
from abc import abstractmethod

from vkbottle.http import ABCSessionManager


class ABCAPI(ABC):
    """ Abstract API class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/low-level/api/api.md
    """

    http: "ABCSessionManager"

    @abstractmethod
    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """

    @abstractmethod
    async def validate_response(self, response: typing.Any) -> typing.Any:
        pass

    @abstractmethod
    async def validate_request(self, request: typing.Any) -> typing.Any:
        pass
