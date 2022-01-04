from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from vkbottle_types.categories import APICategories

if TYPE_CHECKING:
    from vkbottle.http import ABCHTTPClient

    from .request_rescheduler import ABCRequestRescheduler


class ABCAPI(APICategories, ABC):
    """Abstract API class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/api.md
    """

    http_client: "ABCHTTPClient"
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

    @property
    def api_instance(self) -> "ABCAPI":
        return self
