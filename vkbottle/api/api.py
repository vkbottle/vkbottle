from .abc import ABCAPI
from .response_validator import ABCResponseValidator, DEFAULT_RESPONSE_VALIDATORS
from .request_validator import ABCRequestValidator, DEFAULT_REQUEST_VALIDATORS
from vkbottle.http import ABCSessionManager, AiohttpClient, SingleSessionManager
from vkbottle.exception_factory import ABCErrorHandler, ErrorHandler
from vkbottle_types.categories import APICategories
from vkbottle.modules import logger
import typing


APIRequest = typing.NamedTuple("APIRequest", [("method", str), ("data", dict)])


class API(ABCAPI, APICategories):
    """ Default API instance
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/low-level/api/api.md
    """

    API_URL = "https://api.vk.com/method/"
    API_VERSION = "5.103"
    APIRequest = APIRequest

    def __init__(
        self,
        token: str,
        ignore_errors: bool = False,
        session_manager: typing.Optional[SingleSessionManager] = None,
        error_handler: typing.Optional[ABCErrorHandler] = None,
    ):
        self.token = token
        self.ignore_errors = ignore_errors
        self.http: ABCSessionManager = session_manager or SingleSessionManager(AiohttpClient)
        self.error_handler = error_handler or ErrorHandler(redirect_arguments=False)
        self.response_validators: typing.List[ABCResponseValidator] = DEFAULT_RESPONSE_VALIDATORS
        self.request_validators: typing.List[ABCRequestValidator] = DEFAULT_REQUEST_VALIDATORS  # type: ignore

    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """
        async with self.http as session:
            response = await session.request_text(
                "POST",
                self.API_URL + method,
                data=data,  # type: ignore
                params={"access_token": self.token, "v": self.API_VERSION},
            )
            logger.debug(f"Request {method} with {data} data returned {response}")
            return await self.validate_response(response)

    async def request_many(
        self, requests: typing.Iterable[APIRequest]  # type: ignore
    ) -> typing.AsyncIterator[dict]:
        """ Makes many requests opening one session """
        async with self.http as session:
            for request in requests:
                response = await session.request_text(
                    "POST",
                    self.API_URL + request.method,  # type: ignore
                    data=request.data,  # type: ignore # noqa
                    params={"access_token": self.token, "v": self.API_VERSION},  # noqa
                )
                logger.debug(
                    f"Request {request.method} with {request.data} data returned {response}"
                )
                yield await self.validate_response(response)

    async def validate_response(
        self, response: typing.Union[dict, str]
    ) -> typing.Union[dict, typing.NoReturn]:
        """ Validates response from VK,
        to change validations change API.response_validators (list of ResponseValidator's) """
        for validator in self.response_validators:
            response = await validator.validate(response)
        logger.debug("API response was validated")
        return response  # type: ignore

    async def validate_request(self, request: dict) -> dict:
        """ Validates requests from VK,
        to change validations change API.request_validators (list of RequestValidator's) """
        for validator in self.request_validators:
            request = await validator.validate(request)
        logger.debug("API request was validated")
        return request  # type: ignore

    @property
    def api_instance(self) -> "API":
        return self
