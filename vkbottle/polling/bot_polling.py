import asyncio
import enum
from typing import TYPE_CHECKING, AsyncGenerator, Optional

from aiohttp.client_exceptions import ClientConnectionError
from typing_extensions import Self

from vkbottle.exception_factory import ErrorHandler, VKAPIError
from vkbottle.modules import logger

from .abc import ABCPolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class PollingFailureCode(enum.IntEnum):
    HISTORY_OUTDATED = 1
    KEY_EXPIRED = 2
    INFORMATION_LOST = 3


class BotPolling(ABCPolling):
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
        self.wait = wait or 15
        self.rps_delay = rps_delay or 0
        self.stop = False

    async def get_event(self, server: dict) -> dict:
        # sourcery skip: use-fstring-for-formatting
        logger.debug("Making long request to get event with longpoll...")
        return await self.api.http_client.request_json(
            "{}?act=a_check&key={}&ts={}&wait={}&rps_delay={}".format(
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
            self.group_id = (await self.api.request("groups.getById", {}))["response"]["groups"][
                0
            ]["id"]
        return (
            await self.api.request(
                "groups.getLongPollServer",
                {"group_id": self.group_id},
            )
        )["response"]

    async def handle_failed_event(self, server: dict, event: dict) -> dict:
        try:
            failed = PollingFailureCode(event["failed"])
        except ValueError:
            logger.error("Unknown failure code {}, event: {!r}", event["failed"], event)
            return {}

        if failed == PollingFailureCode.HISTORY_OUTDATED:
            server["ts"] = event["ts"]
            return server

        if failed in (PollingFailureCode.KEY_EXPIRED, PollingFailureCode.INFORMATION_LOST):
            new_server = await self.get_server()
            new_server["ts"] = (
                server["ts"] if failed == PollingFailureCode.KEY_EXPIRED else new_server["ts"]
            )
            return new_server

        return {}

    async def listen(self) -> AsyncGenerator[dict, None]:
        retry_count = 0
        server = await self.get_server()
        logger.debug("Starting listening to Longpoll")

        while not self.stop:
            try:
                server = server if server else await self.get_server()
                event = await self.get_event(server)

                if "failed" in event:
                    server = await self.handle_failed_event(server, event)
                    continue

                if "ts" not in event:
                    server = await self.get_server()
                    continue

                server["ts"] = event["ts"]
                retry_count = 0
                yield event
            except (ClientConnectionError, asyncio.TimeoutError, VKAPIError[10]):
                logger.error("Unable to make request to Longpoll, retrying...")
                retry_count += 1
                server = {}
                await asyncio.sleep(0.1 * retry_count)
            except Exception as e:
                await self.error_handler.handle(e)

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
