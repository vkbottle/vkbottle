from typing import Optional, AsyncIterator
from ..modules import logger
from .abc import ABCPolling
from .. import ABCAPI

URL = "https://{}?act=a_check&key={}&ts={}&wait={}&mode={}&version={}"


class UserPolling(ABCPolling):
    """ User Polling class """

    def __init__(
        self,
        api: Optional[ABCAPI] = None,
        user_id: Optional[int] = None,
        wait: Optional[int] = None,
        version: Optional[int] = None,
        mode: Optional[int] = None
    ):
        self._api = api
        self.user_id = user_id
        self.wait = wait or 15
        self.version = version or 3
        self.mode = mode or 128
        self.stop = False

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")
        return (await self.api.request("messages.getLongPollServer", {}))["response"]

    async def get_event(self, server: dict) -> dict:
        logger.debug("Making long request to get event with User Long Poll API...")
        async with self.api.http as session:
            return await session.request_json(
                "POST",
                URL.format(
                    server["server"], server["key"], server["ts"], self.wait, self.mode, self.version
                )
            )

    async def listen(self) -> AsyncIterator[dict]:
        server = await self.get_server()
        logger.debug("Start listening to LongPoll...")
        while not self.stop:
            event = await self.get_event(server)
            if not event.get("ts"):
                server = await self.get_server()
                continue

            server["ts"] = event["ts"]
            yield event

    def construct(self, api: "ABCAPI") -> "ABCPolling":
        self._api = api
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

