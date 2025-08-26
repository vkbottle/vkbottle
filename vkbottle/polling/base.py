import asyncio
import enum
from abc import ABC
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Optional

from aiohttp.client_exceptions import ClientConnectionError

from vkbottle.exception_factory import VKAPIError
from vkbottle.modules import logger
from vkbottle.polling.abc import ABCPolling

if TYPE_CHECKING:
    from vkbottle.exception_factory import ABCErrorHandler


class FailureCode(enum.IntEnum):
    HISTORY_OUTDATED = 1
    KEY_EXPIRED = 2
    INFORMATION_LOST = 3
    INVALID_VERSION = 4


class BasePolling(ABCPolling, ABC):
    stop: bool
    error_handler: "ABCErrorHandler"
    lp_version: Optional[int] = None

    async def handle_failed_event(self, server: dict, event: dict) -> dict:
        try:
            failed = FailureCode(event["failed"])
        except ValueError:
            logger.error("Unknown failure code {!r}, event: {!r}", event["failed"], event)
            return {}

        if failed == FailureCode.HISTORY_OUTDATED:
            server["ts"] = event["ts"]
            return server

        if failed in (FailureCode.KEY_EXPIRED, FailureCode.INFORMATION_LOST):
            new_server = await self.get_server()
            new_server["ts"] = (
                server["ts"] if failed == FailureCode.KEY_EXPIRED else new_server["ts"]
            )
            return new_server

        if failed == FailureCode.INVALID_VERSION:
            logger.error(
                "Invalid version of longpoll, min: {}, max: {}. Using version 3.",
                event["min_version"],
                event["max_version"],
            )
            self.lp_version = 3
            return await self.get_server()

        return {}

    async def listen(self) -> AsyncGenerator[dict, None]:
        retry_count = 0
        server = await self.get_server()
        logger.debug("Starting listening to {} longpoll", self.__class__.__name__)

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
                if "updates" not in event:
                    continue
                yield event
            except (ClientConnectionError, asyncio.TimeoutError, VKAPIError[10]):
                logger.error("Unable to make request to {}, retrying...", self.__class__.__name__)
                retry_count += 1
                server = {}
                await asyncio.sleep(0.1 * retry_count)
            except Exception as e:
                await self.error_handler.handle(e)


__all__ = ("BasePolling", "FailureCode")
