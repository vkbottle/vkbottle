from typing import Any, List, Callable

from vkbottle_types.events import GroupEventType

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware, MiddlewareResponse
from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.modules import logger
from vkbottle.tools.dev_tools import message_min
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from ..abc import ABCView


class MessageView(ABCView):
    def __init__(self):
        self.handlers: List["ABCHandler"] = []
        self.middlewares: List["BaseMiddleware"] = []
        self.default_text_approximators: List[Callable[[MessageMin], str]] = []
        self.handler_return_manager = BotMessageReturnHandler()

    async def process_event(self, event: dict) -> bool:
        if GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW:
            return True

    async def handle_event(self, event: dict, ctx_api: "ABCAPI") -> Any:
        logger.debug(f"Handling event ({event.get('event_id')}) with message view")
        context_variables = {}
        message = message_min(event, ctx_api)

        for text_ax in self.default_text_approximators:
            message.text = text_ax(message)

        for middleware in self.middlewares:
            response = await middleware.pre(message)
            if response == MiddlewareResponse(False):
                return []
            elif isinstance(response, dict):
                context_variables.update(response)

        handle_responses = []
        for handler in self.handlers:
            result = await handler.filter(message)
            logger.debug(f"Handler {handler} returned {result}")

            if result is False:
                continue
            elif not isinstance(result, dict):
                result = {}

            handler_response = await handler.handle(message, **result, **context_variables)
            handle_responses.append(handler_response)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager,
                    handler_response,
                    message,
                    {**result, **context_variables},
                )

            if handler.blocking:
                return

        for middleware in self.middlewares:
            await middleware.post(message, self, handle_responses)
