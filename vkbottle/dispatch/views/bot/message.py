from typing import Any, List

from vkbottle_types.events import GroupEventType

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware, MiddlewareResponse
from vkbottle.modules import logger
from vkbottle.tools.dev_tools import message_min
from ..abc import ABCView


class MessageView(ABCView):
    def __init__(self):
        self.handlers: List["ABCHandler"] = []
        self.middlewares: List["BaseMiddleware"] = []

    async def process_event(self, event: dict) -> bool:
        if GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW:
            return True

    async def handle_event(self, event: dict, ctx_api: "ABCAPI") -> Any:
        logger.debug("Handling event ({}) with message view".format(event.get("event_id")))
        context_variables = {}
        message = message_min(event, ctx_api)

        for middleware in self.middlewares:
            response = await middleware.pre(message)
            if response == MiddlewareResponse(False):
                return []
            elif isinstance(response, dict):
                context_variables.update(response)

        handle_responses = []
        for handler in self.handlers:
            result = await handler.filter(message)
            logger.debug("Handler {} returned {}".format(handler, result))

            if result is False:
                continue
            elif not isinstance(result, dict):
                result = {}

            handle_responses.append(await handler.handle(message, **result))
            if handler.blocking:
                return handle_responses

        for middleware in self.middlewares:
            await middleware.post(message, self, handle_responses)

        return handle_responses
