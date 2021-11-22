import asyncio
import typing
from abc import ABC
from typing import Any, Callable, List, Optional

from vkbottle_types.events import GroupEventType

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware, MiddlewareResponse
from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.rules.abc import ABCRule
from vkbottle.modules import logger
from vkbottle.tools.dev_tools import message_min
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle.tools.dev_tools.waiter import Waiter

from ..abc_dispense import ABCDispenseView

DEFAULT_STATE_KEY = "peer_id"


class ABCMessageView(ABCDispenseView, ABC):
    def __init__(self):
        self.state_source_key = DEFAULT_STATE_KEY
        self.handlers: List["ABCHandler"] = []
        self.middlewares: List["BaseMiddleware"] = []
        self.default_text_approximators: List[Callable[[MessageMin], str]] = []
        self.handler_return_manager = BotMessageReturnHandler()
        self.waiters: typing.Dict[int, Waiter] = {}

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW

    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI"
    ) -> Any:

        logger.debug("Handling event ({}) with message view".format(event.get("event_id")))
        context_variables = {}
        message = message_min(event, ctx_api)

        for text_ax in self.default_text_approximators:
            message.text = text_ax(message)

        for middleware in self.middlewares:
            response = await middleware.pre(message)
            if response == MiddlewareResponse(False):
                return
            elif isinstance(response, dict):
                context_variables.update(response)

        if message.peer_id in self.waiters:
            waiter = self.waiters[message.peer_id]
            checks = [await rule.check(message) not in (None, False) for rule in waiter.rules]

            if all(checks):
                self.waiters.pop(message.peer_id)
                setattr(waiter.event, "e", message)
                waiter.event.set()
                return

            if not waiter.default:
                return

            w_handler = self.handler_return_manager.get_handler(waiter.default)

            if w_handler:
                await w_handler(
                    self.handler_return_manager, waiter.default, message, context_variables
                )
                return

            response = await waiter.default(message, **context_variables)

            for middleware in self.middlewares:
                await middleware.post(message, self, [response], [])

            return

        handle_responses = []
        handlers = []

        for handler in self.handlers:
            result = await handler.filter(message)
            logger.debug("Handler {} returned {}".format(handler, result))

            if result is False:
                continue

            elif isinstance(result, dict):
                context_variables.update(result)

            handler_response = await handler.handle(message, **context_variables)
            handle_responses.append(handler_response)
            handlers.append(handler)

            return_handler = self.handler_return_manager.get_handler(handler_response)
            if return_handler is not None:
                await return_handler(
                    self.handler_return_manager, handler_response, message, context_variables
                )

            if handler.blocking:
                break

        for middleware in self.middlewares:
            await middleware.post(message, self, handle_responses, handlers)

    async def wait_for(
        self,
        m: MessageMin,
        *rules: ABCRule,
        default: typing.Optional[typing.Callable[..., None]] = None,
    ) -> MessageMin:
        event = asyncio.Event()
        self.waiters[m.peer_id] = Waiter(list(rules), event, default)
        await event.wait()
        return getattr(event, "e")  # noqa


class MessageView(ABCMessageView):
    def get_state_key(self, event: dict) -> Optional[int]:
        return event["object"]["message"].get(self.state_source_key)
