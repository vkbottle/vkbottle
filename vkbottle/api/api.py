import typing

from vkbottle_types.categories import APICategories

from vkbottle.http import ABCSessionManager, AiohttpClient, SingleSessionManager
from vkbottle.modules import logger

from .abc import ABCAPI
from .request_rescheduler import ABCRequestRescheduler, BlockingRequestRescheduler
from .request_validator import DEFAULT_REQUEST_VALIDATORS, ABCRequestValidator
from .response_validator import DEFAULT_RESPONSE_VALIDATORS, ABCResponseValidator
from .token_generator import Token, get_token_generator

APIRequest = typing.NamedTuple("APIRequest", [("method", str), ("data", dict)])


class API(ABCAPI, APICategories):
    """ Default API instance
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/api/api.md
    """

    API_URL = "https://api.vk.com/method/"
    API_VERSION = "5.103"
    APIRequest = APIRequest

    def __init__(
        self,
        token: Token,
        ignore_errors: bool = False,
        session_manager: typing.Optional[SingleSessionManager] = None,
        request_rescheduler: typing.Optional[ABCRequestRescheduler] = None,
    ):
        self.token_generator = get_token_generator(token)
        self.ignore_errors = ignore_errors
        self.http: ABCSessionManager = session_manager or SingleSessionManager(AiohttpClient)
        self.request_rescheduler = request_rescheduler or BlockingRequestRescheduler()
        self.response_validators: typing.List[ABCResponseValidator] = DEFAULT_RESPONSE_VALIDATORS
        self.request_validators: typing.List[ABCRequestValidator] = DEFAULT_REQUEST_VALIDATORS  # type: ignore

    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """
        data = await self.validate_request(data)

        async with self.http as session:
            async with self.token_generator as token:
                response = await session.request_text(
                    "POST",
                    self.API_URL + method,
                    data=data,  # type: ignore
                    params={"access_token": token, "v": self.API_VERSION},
                )
            logger.debug("Request {} with {} data returned {}".format(method, data, response))
            return await self.validate_response(method, data, response)

    async def request_many(
        self, requests: typing.Iterable[APIRequest]  # type: ignore
    ) -> typing.AsyncIterator[dict]:
        """ Makes many requests opening one session """
        async with self.http as session:
            for request in requests:
                method, data = request.method, await self.validate_request(request.data)  # type: ignore
                async with self.token_generator as token:
                    response = await session.request_text(
                        "POST",
                        self.API_URL + method,
                        data=data,  # noqa
                        params={"access_token": token, "v": self.API_VERSION},  # noqa
                    )
                logger.debug("Request {} with {} data returned {}".format(method, data, response))
                yield await self.validate_response(method, data, response)

    async def validate_response(
        self, method: str, data: dict, response: typing.Union[dict, str]
    ) -> typing.Union[typing.Any, typing.NoReturn]:
        """ Validates response from VK,
        to change validations change API.response_validators (list of ResponseValidator's) """
        for validator in self.response_validators:
            response = await validator.validate(method, data, response, self)
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

    def __repr__(self) -> str:
        return f"<API token_generator={self.token_generator}...>"
