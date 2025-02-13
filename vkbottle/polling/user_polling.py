from typing import TYPE_CHECKING, Optional

from vkbottle.exception_factory import ErrorHandler
from vkbottle.modules import logger

from .base import BasePolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class UserPolling(BasePolling):
    """User Polling class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/polling
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
        # sourcery skip: use-fstring-for-formatting
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
            msg = (
                "You must construct polling with API before try to access api property of Polling"
            )
            raise NotImplementedError(msg)
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI"):
        self._api = new_api


__all__ = ("UserPolling",)
