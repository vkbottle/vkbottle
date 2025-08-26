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
        group_id: Optional[int] = None,
        wait: Optional[int] = None,
        mode: Optional[int] = None,
        rps_delay: Optional[int] = None,
        lp_version: Optional[int] = None,
        need_pts: Optional[bool] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ) -> None:
        self._api = api
        self.error_handler = error_handler or ErrorHandler()
        self.user_id = user_id
        self.group_id = group_id
        self.wait = min(wait or 25, 90)
        self.mode = mode or 234
        self.rps_delay = rps_delay or 0
        self.lp_version = lp_version or 3
        self.need_pts = need_pts
        self.stop = False

    async def get_event(self, server: dict) -> dict:
        # sourcery skip: use-fstring-for-formatting
        logger.debug("Making long request to get event with longpoll...")
        return await self.api.http_client.request_json(
            url="https://{}?act=a_check&key={}&ts={}&wait={}&mode={}&rps_delay={}&version={}".format(
                server["server"],
                server["key"],
                server["ts"],
                self.wait,
                self.mode,
                self.rps_delay,
                self.lp_version,
            ),
            method="POST",
        )

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")

        if self.user_id is None:
            response = (await self.api.request("users.get", {}))["response"]
            if not response:
                msg = "Unable to get user id for user polling. Perhaps you are using a group access token?"
                raise RuntimeError(msg)

            self.user_id = response[0]["id"]

        return (
            await self.api.request(
                "messages.getLongPollServer",
                {
                    "need_pts": self.need_pts,
                    "version": self.lp_version,
                    "group_id": self.group_id,
                },
            )
        )["response"]

    def construct(
        self,
        api: "ABCAPI",
        error_handler: Optional["ABCErrorHandler"] = None,
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
