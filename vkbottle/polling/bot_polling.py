from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from vkbottle.exception_factory import ErrorHandler
from vkbottle.modules import logger

from .base import BasePolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class BotPolling(BasePolling):
    """Bot Polling class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/polling
    """

    def __init__(
        self,
        api: Optional["ABCAPI"] = None,
        group_id: Optional[int] = None,
        wait: Optional[int] = None,
        rps_delay: Optional[int] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ) -> None:
        self._api = api
        self.error_handler = error_handler or ErrorHandler()
        self.group_id = group_id
        self.wait = min(wait or 25, 90)
        self.rps_delay = rps_delay or 0
        self.stop = False

    async def get_event(self, server: dict) -> dict:
        # sourcery skip: use-fstring-for-formatting
        logger.debug("Making long request to get event with longpoll...")
        return await self.api.http_client.request_json(
            url="{}?act=a_check&key={}&ts={}&wait={}&rps_delay={}".format(
                server["server"],
                server["key"],
                server["ts"],
                self.wait,
                self.rps_delay,
            ),
            method="POST",
        )

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")
        if self.group_id is None:
            response = (await self.api.request("groups.getById", {}))["response"]
            if not response.get("groups", []):
                msg = "Unable to get group id for bot polling. Perhaps you are using a user access token?"
                raise RuntimeError(msg)

            self.group_id = response["groups"][0]["id"]

        return (
            await self.api.request(
                "groups.getLongPollServer",
                {"group_id": self.group_id},
            )
        )["response"]

    def construct(
        self,
        api: "ABCAPI",
        error_handler: Optional["ABCErrorHandler"] = None,
    ) -> Self:
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
    def api(self, new_api: "ABCAPI") -> None:
        self._api = new_api


__all__ = ("BotPolling",)
