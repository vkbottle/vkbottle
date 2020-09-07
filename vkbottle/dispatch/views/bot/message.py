from ..abc import ABCView
from vkbottle_types.events import GroupEventType
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.api.abc import ABCAPI
from vkbottle.tools.dev_tools import message_min
from typing import Any, List


class MessageView(ABCView):
    handlers: List["ABCHandler"] = []
    middleware: List["BaseMiddleware"] = []

    async def process_event(self, event: dict) -> bool:
        if GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW:
            return True

    async def handle_event(self, event: dict, ctx_api: "ABCAPI") -> Any:
        message = message_min(event, ctx_api)

        handle_responses = []
        for handler in self.handlers:
            result = await handler.filter(message)

            if result is False:
                continue
            elif not isinstance(result, dict):
                result = {}

            handle_responses.append(await handler.handle(message, **result))
            if handler.blocking:
                return handle_responses

        return handle_responses
