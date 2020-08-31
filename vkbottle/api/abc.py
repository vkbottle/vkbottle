from abc import ABC, abstractmethod
from vkbottle.http import ABCSessionManager
import typing


class ABCAPI(ABC):
    """ Abstract API class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/api.md
    """

    http: "ABCSessionManager"

    @abstractmethod
    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """
        pass

    @abstractmethod
    async def validate_response(self, response: typing.Any) -> typing.Any:
        pass

    @abstractmethod
    async def validate_request(self, request: typing.Any) -> typing.Any:
        pass
