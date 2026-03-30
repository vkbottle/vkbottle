from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from typing_extensions import Self
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
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api
    """

    token_generator: "ABCTokenGenerator"
    ignore_errors: bool
    http_client: "ABCHTTPClient"
    request_rescheduler: "ABCRequestRescheduler"
    response_validators: list["ABCResponseValidator"]
    request_validators: list["ABCRequestValidator"]
    captcha_handler: Callable[["CaptchaError"], Awaitable[Any]] | None = None

    @abstractmethod
    async def request(
        self,
        method: str,
        data: dict[str, Any],
        version: str | None = None,
    ) -> dict[str, Any]:
        """Makes a single request opening a session"""

    @abstractmethod
    async def validate_response(self, method: str, data: dict[str, Any], response: Any) -> Any:
        pass

    @abstractmethod
    async def validate_request(self, request: Any) -> Any:
        pass

    @property
    def api_instance(self) -> Self:
        return self
