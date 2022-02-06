from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Awaitable, Callable, List, Optional

from vkbottle_types.categories import APICategories

if TYPE_CHECKING:
    from vkbottle.exception_factory import CaptchaError
    from vkbottle.http import ABCHTTPClient

    from .request_rescheduler import ABCRequestRescheduler
    from .request_validator import ABCRequestValidator
    from .response_validator import ABCResponseValidator
    from .token_generator import ABCTokenGenerator


class ABCAPI(APICategories, ABC):
    """Abstract API class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/api.md
    """

    token_generator: "ABCTokenGenerator"
    ignore_errors: bool
    http_client: "ABCHTTPClient"
    request_rescheduler: "ABCRequestRescheduler"
    response_validators: List["ABCResponseValidator"]
    request_validators: List["ABCRequestValidator"]
    captcha_handler: Optional[Callable[["CaptchaError"], Awaitable]] = None

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
