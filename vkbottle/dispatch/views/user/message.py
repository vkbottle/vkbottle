from abc import ABC
from typing import Optional

from vkbottle_types.events import UserEventType

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.modules import logger
from vkbottle.tools.dev_tools.mini_types.user import MessageMin, message_min

from ..abc_dispense import ABCDispenseView


class ABCMessageView(ABCDispenseView, ABC):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = UserMessageReturnHandler()

    async def process_event(self, event: int) -> bool:
        return UserEventType(event) == UserEventType.NEW_MESSAGE

    # TODO: List[???]
    async def handle_event(
        self, event: list, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> None:
        logger.debug("Handling event ({}) with message view".format(event[0]))
        context_variables: dict = {}
        message = await message_min(event[1], ctx_api)
        message.state_peer = await state_dispenser.cast(self.get_state_key(message))

        for text_ax in self.default_text_approximators:
            message.text = text_ax(message)

        error = await self.pre_middleware(message, context_variables)
        if error:
            logger.info("Handling stopped, pre_middleware returned error")
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

        await self.post_middleware(handle_responses, handlers)


class MessageView(ABCMessageView):
    def get_state_key(self, message: MessageMin) -> Optional[int]:
        return getattr(message, self.state_source_key, None)
