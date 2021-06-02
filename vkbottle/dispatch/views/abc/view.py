from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Set, Type

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.dispatch.return_manager import BaseReturnManager
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle_types.events import Event

DEFAULT_STATE_KEY = "peer_id"


class ABCView(ABC):
    handlers: List["ABCHandler"]
    middlewares: Set[Type["BaseMiddleware"]]
    middleware_instances: List["BaseMiddleware"]
    handler_return_manager: BaseReturnManager

    @abstractmethod
    def __init__(self):
        self.handlers = []
        self.middlewares = set()
        self.middleware_instances = []
        self.handler_return_manager = None

    @abstractmethod
    async def process_event(self, event: "Event") -> bool:
        pass

    async def pre_middleware(
        self,
        event: "Event",
        context_variables: Optional[dict] = None,
    ) -> Optional[Exception]:
        """Run all of the pre middleware methods and return an exception if any error occurs"""
        self.middleware_instances.clear()
        for middleware in self.middlewares:
            mw_instance = middleware(event, view=self)
            await mw_instance.pre()
            if not mw_instance.can_forward:
                logger.debug(f"{mw_instance} pre returned error {mw_instance.error}")
                return mw_instance.error

            self.middleware_instances.append(mw_instance)
            if context_variables is not None:
                context_variables.update(mw_instance.context_update)

    async def post_middleware(
        self,
        handle_responses: Optional[List] = None,
        handlers: Optional[List["ABCHandler"]] = None,
    ):
        for middleware in self.middleware_instances:
            # Update or leave value
            middleware.handle_responses = handle_responses or middleware.handle_responses
            middleware.handlers = handlers or middleware.handlers

            await middleware.post()
            if not middleware.can_forward:
                logger.debug(f"{middleware} post returned error {middleware.error}")
                return middleware.error

    @abstractmethod
    async def handle_event(
        self,
        event: "Event",
        ctx_api: "ABCAPI",
        state_dispenser: "ABCStateDispenser",
    ) -> None:
        pass

    def register_middleware(self, middleware: Type["BaseMiddleware"]):
        try:
            if not issubclass(middleware, (BaseMiddleware,)):
                raise ValueError("Argument is not a subclass of BaseMiddleware")
        except TypeError:
            raise ValueError("Argument is not a class")
        self.middlewares.add(middleware)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"handlers={self.handlers} "
            f"middlewares={self.middlewares} "
            f"handler_return_manager={self.handler_return_manager}"
        )
