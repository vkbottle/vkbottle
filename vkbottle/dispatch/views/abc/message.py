from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Generic, List, TypeVar

from vkbottle.modules import logger

from .dispense import ABCDispenseView

if TYPE_CHECKING:
    from vkbottle.api.abc import ABCAPI
    from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
    from vkbottle.dispatch.handlers import ABCHandler
    from vkbottle.tools.dev.mini_types.base import BaseMessageMin

DEFAULT_STATE_KEY = "peer_id"


T_contra = TypeVar("T_contra", list, dict, contravariant=True)
F_contra = TypeVar("F_contra", contravariant=True)


class ABCMessageView(ABCDispenseView[T_contra, F_contra], ABC, Generic[T_contra, F_contra]):
    handlers: List["ABCHandler"]
    state_source_key: str
    default_text_approximators: List[Callable[["BaseMessageMin"], str]]

    def __init__(self):
        super().__init__()
        self.state_source_key = DEFAULT_STATE_KEY
        self.default_text_approximators = []

    @staticmethod
    @abstractmethod
    def get_event_type(event: T_contra) -> Any:
        pass

    @staticmethod
    @abstractmethod
    async def get_message(event: T_contra, ctx_api) -> Any:
        pass

    async def handle_event(
        self, event: T_contra, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> None:
        # For user event mapping, consider checking out
        # https://dev.vk.com/api/user-long-poll/getting-started
        logger.debug("Handling event ({}) with message view".format(self.get_event_type(event)))
        context_variables: dict = {}
        message = await self.get_message(event, ctx_api)
        message.state_peer = await state_dispenser.cast(self.get_state_key(message))

        for text_ax in self.default_text_approximators:
            message.text = text_ax(message)

        mw_instances = await self.pre_middleware(message, context_variables)
        if mw_instances is None:
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

        await self.post_middleware(mw_instances, handle_responses, handlers)
