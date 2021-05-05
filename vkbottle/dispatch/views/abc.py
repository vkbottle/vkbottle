from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, Set, Type

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.dispatch.return_manager import BaseReturnManager
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCView(ABC):
    handlers: List["ABCHandler"]
    middlewares: Set[Type["BaseMiddleware"]]
    middleware_instances: List["BaseMiddleware"]
    handler_return_manager: BaseReturnManager

    @abstractmethod
    async def process_event(self, event: "Event") -> bool:
        pass

    async def pre_middleware(self, event: "Event", context_variables: dict) -> Optional[Exception]:
        """Run all of the pre middleware methods and return an exception if any error occurs"""
        self.middleware_instances.clear()
        for middleware in self.middlewares:
            mw_instance = middleware(event)
            await mw_instance.pre()
            if not mw_instance.can_forward:
                logger.debug(f"{mw_instance} returned error {mw_instance.error}")
                return mw_instance.error

            self.middleware_instances.append(mw_instance)
            context_variables.update(mw_instance.context_update)

    async def post_middleware(
        self, view: "ABCView", handle_responses: List[Any], handlers: List["ABCHandler"]
    ):
        for middleware in self.middleware_instances:
            await middleware.post(view, handle_responses, handlers)

    @abstractmethod
    async def handle_event(
        self, event: "Event", ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
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
