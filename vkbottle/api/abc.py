from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from vkbottle.http import ABCSessionManager

    from .request_rescheduler import ABCRequestRescheduler


class ABCAPI(ABC):
    """Abstract API class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/api.md
    """

    http: "ABCSessionManager"
    ignore_errors: bool
    request_rescheduler: "ABCRequestRescheduler"

    @abstractmethod
    async def request(self, method: str, data: dict) -> dict:
        """Makes a single request opening a session"""

    @abstractmethod
    async def validate_response(self, method: str, data: dict, response: Any) -> Any:
        pass

    @abstractmethod
    async def validate_request(self, request: Any) -> Any:
        pass
