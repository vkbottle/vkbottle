from typing import TYPE_CHECKING, AsyncIterator, Optional

from aiohttp.client_exceptions import ServerConnectionError

from vkbottle.exception_factory import ErrorHandler
from vkbottle.modules import logger

from .abc import ABCPolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class UserPolling(ABCPolling):
    """User Polling class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/polling/polling.md
    """

    def __init__(
        self,
        api: Optional["ABCAPI"] = None,
        user_id: Optional[int] = None,
        wait: Optional[int] = None,
        mode: Optional[int] = None,
        rps_delay: Optional[int] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        self._api = api
        self.error_handler = error_handler or ErrorHandler()
        self.user_id = user_id
        self.wait = wait or 15
        self.mode = mode or 234
        self.rps_delay = rps_delay or 0
        self.stop = False

    async def get_event(self, server: dict) -> dict:
        logger.debug("Making long request to get event with longpoll...")
        return await self.api.http_client.request_json(
            "https://{}?act=a_check&key={}&ts={}&wait={}&mode={}&rps_delay={}".format(
                server["server"],
                server["key"],
                server["ts"],
                self.wait,
                self.mode,
                self.rps_delay,
            ),
            method="POST",
        )

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")
        if self.user_id is None:
            self.user_id = (await self.api.request("users.get", {}))["response"][0]["id"]
        return (await self.api.request("messages.getLongPollServer", {}))["response"]

    async def listen(self) -> AsyncIterator[dict]:  # type: ignore
        server = await self.get_server()
        logger.debug("Starting listening to longpoll")
        while not self.stop:
            try:
                event = await self.get_event(server)
                if not event.get("ts"):
                    server = await self.get_server()
                    continue
                server["ts"] = event["ts"]
                yield event
            except ServerConnectionError:
                server = await self.get_server()
            except BaseException as e:
                await self.error_handler.handle(e)

    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "UserPolling":
        self._api = api
        if error_handler is not None:
            self.error_handler = error_handler
        return self

    @property
    def api(self) -> "ABCAPI":
        if self._api is None:
            raise NotImplementedError(
                "You must construct polling with API before try to access api property of Polling"
            )
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI"):
        self._api = new_api
