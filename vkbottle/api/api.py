from .abc import ABCAPI
from vkbottle.http import ABCSessionManager, SessionManager, AiohttpClient
import typing


APIRequest = typing.NamedTuple("APIRequest", [("method", str), ("data", dict)])


class API(ABCAPI):
    """ Default API instance
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/api.md
    """

    API_URL = "https://api.vk.com/method/"
    API_VERSION = "5.103"
    APIRequest = APIRequest

    def __init__(
        self,
        token: str,
        ignore_errors: bool = False,
        session_manager: typing.Optional[SessionManager] = None,
    ):
        self.token = token
        self.ignore_errors = ignore_errors
        self.http: ABCSessionManager = session_manager or SessionManager(AiohttpClient)

    async def request(self, method: str, data: dict) -> dict:
        """ Makes a single request opening a session """
        async with self.http as session:
            response = await session.request_json(
                "GET",
                self.API_URL + method,
                data=data,
                params={"access_token": self.token, "v": self.API_VERSION},
            )
            return response

    async def request_many(
        self, requests: typing.Iterable[APIRequest]
    ) -> typing.AsyncIterator[dict]:
        """ Makes many requests opening one session """
        async with self.http as session:
            for request in requests:
                yield await session.request_text(
                    "GET",
                    self.API_URL + request.method,
                    data=request.data,
                    params={"access_token": self.token, "v": self.API_VERSION},
                )

    async def validate_response(self, response: dict) -> typing.Any:
        pass
