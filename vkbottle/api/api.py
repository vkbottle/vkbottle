import typing
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Iterable,
    List,
    NamedTuple,
    NoReturn,
    Optional,
    Union,
)

import vkbottle_types

from vkbottle.exception_factory import CaptchaError
from vkbottle.http import SingleAiohttpClient
from vkbottle.modules import logger

from .abc import ABCAPI
from .request_rescheduler import BlockingRequestRescheduler
from .request_validator import DEFAULT_REQUEST_VALIDATORS
from .response_validator import DEFAULT_RESPONSE_VALIDATORS
from .token_generator import get_token_generator

if TYPE_CHECKING:
    from vkbottle.http import ABCHTTPClient

    from .request_rescheduler import ABCRequestRescheduler
    from .request_validator import ABCRequestValidator
    from .response_validator import ABCResponseValidator
    from .token_generator import Token

APIRequest = NamedTuple("APIRequest", [("method", str), ("data", dict)])
CaptchaHandler = typing.Callable[[CaptchaError], typing.Awaitable]


class API(ABCAPI):
    """Default API instance
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/api.md
    """

    API_URL = vkbottle_types.API_URL
    API_VERSION = vkbottle_types.API_VERSION
    APIRequest = APIRequest

    def __init__(
        self,
        token: "Token",
        ignore_errors: bool = False,
        http_client: Optional["ABCHTTPClient"] = None,
        request_rescheduler: Optional["ABCRequestRescheduler"] = None,
    ):
        self.token_generator = get_token_generator(token)
        self.ignore_errors = ignore_errors
        self.http_client = http_client or SingleAiohttpClient()
        self.request_rescheduler = request_rescheduler or BlockingRequestRescheduler()
        self.response_validators: List["ABCResponseValidator"] = DEFAULT_RESPONSE_VALIDATORS
        self.request_validators: List["ABCRequestValidator"] = DEFAULT_REQUEST_VALIDATORS  # type: ignore
        self.captcha_handler: Optional["CaptchaHandler"] = None

    async def request(self, method: str, data: dict) -> dict:
        """Makes a single request opening a session"""
        data = await self.validate_request(data)

        async with self.token_generator as token:
            response = await self.http_client.request_text(
                self.API_URL + method,
                method="POST",
                data=data,  # type: ignore
                params={"access_token": token, "v": self.API_VERSION},
            )
        logger.debug("Request {} with {} data returned {}".format(method, data, response))
        return await self.validate_response(method, data, response)  # type: ignore

    async def request_many(
        self, requests: Iterable[APIRequest]  # type: ignore
    ) -> AsyncIterator[dict]:
        """Makes many requests opening one session"""
        for request in requests:
            method, data = request.method, await self.validate_request(request.data)  # type: ignore
            async with self.token_generator as token:
                response = await self.http_client.request_json(
                    self.API_URL + method,
                    method="POST",
                    data=data,  # noqa
                    params={"access_token": token, "v": self.API_VERSION},  # noqa
                )
            logger.debug("Request {} with {} data returned {}".format(method, data, response))
            yield await self.validate_response(method, data, response)  # type: ignore

    async def validate_response(
        self, method: str, data: dict, response: Union[dict, str]
    ) -> Union[Any, NoReturn]:
        """Validates response from VK,
        to change validations change API.response_validators (list of ResponseValidator's)"""
        for validator in self.response_validators:
            response = await validator.validate(method, data, response, self)  # type: ignore
        logger.debug("API response was validated")
        return response  # type: ignore

    async def validate_request(self, request: dict) -> dict:
        """Validates requests from VK,
        to change validations change API.request_validators (list of RequestValidator's)"""
        for validator in self.request_validators:
            request = await validator.validate(request)  # type: ignore
        logger.debug("API request was validated")
        return request  # type: ignore

    def add_captcha_handler(self, handler: CaptchaHandler) -> CaptchaHandler:
        self.captcha_handler = handler
        return handler

    def __repr__(self) -> str:
        return f"<API token_generator={self.token_generator}...>"
