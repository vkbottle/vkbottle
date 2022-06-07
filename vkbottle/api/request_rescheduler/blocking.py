from time import sleep as blocking_sleep
from typing import TYPE_CHECKING, Any, Union

from vkbottle.modules import logger

from .abc import ABCRequestRescheduler

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


DEFAULT_DELAY = 5


class BlockingRequestRescheduler(ABCRequestRescheduler):
    def __init__(self, delay: int = DEFAULT_DELAY):
        self.delay = delay

    async def reschedule(
        self,
        ctx_api: Union["ABCAPI", "API"],
        method: str,
        data: dict,
        recent_response: Any,
    ) -> dict:
        logger.debug(
            "Usage of blocking rescheduler is assumed when VK doesn't respond to "
            "all requests for an amount of time. Starting..."
        )

        attempt_number = 1
        while not isinstance(recent_response, dict):
            logger.info("Attempt number {}. Making request...", attempt_number)
            blocking_sleep(self.delay * attempt_number)
            recent_response = await ctx_api.request(method, data)
            attempt_number += 1
            logger.debug("Attempt succeed? - {}", isinstance(recent_response, dict))

        logger.info("Finally succeed after {} seconds", self.delay * attempt_number)
        return recent_response
