from abc import ABC, abstractmethod
from vkbottle.http import ABCSessionManager
import typing

if typing.TYPE_CHECKING:
    from .api_error_handler import ABCAPIErrorHandler
    from .request_rescheduler import ABCRequestRescheduler


class ABCAPI(ABC):
    """ Abstract API class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/low-level/api/api.md
    """

    http: "ABCSessionManager"
    ignore_errors: bool
    api_error_handler: "ABCAPIErrorHandler"
    request_rescheduler: "ABCRequestRescheduler"

    @abstractmethod
    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """
        pass

    @abstractmethod
    async def validate_response(self, method: str, data: dict, response: typing.Any) -> typing.Any:
        pass

    @abstractmethod
    async def validate_request(self, request: typing.Any) -> typing.Any:
        pass
