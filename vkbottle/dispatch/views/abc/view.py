from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.modules import logger
from vkbottle.tools.dev.utils import call_by_signature

if TYPE_CHECKING:
    from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
    from vkbottle.dispatch.handlers import ABCHandler
    from vkbottle.dispatch.return_manager import BaseReturnManager

    Handlers = Union[List["ABCHandler"], Dict[Any, List]]

T_contra = TypeVar("T_contra", list, dict, contravariant=True)


class ABCView(ABC, Generic[T_contra]):
    handlers: "Handlers"
    middlewares: List[Type["BaseMiddleware"]]
    handler_return_manager: "BaseReturnManager"

    @abstractmethod
    def __init__(self):
        self.handlers = []
        self.middlewares = []
        self.handler_return_manager = None  # type: ignore

    @abstractmethod
    async def process_event(self, event: T_contra) -> bool:
        pass

    async def pre_middleware(
        self,
        event: T_contra,
        context_variables: Optional[dict] = None,
    ) -> Optional[List[BaseMiddleware]]:
        """Run all of the pre middleware methods and return an exception if any error occurs"""
        mw_instances = []

        for middleware in self.middlewares:
            mw_instance = middleware(event, view=self)
            await call_by_signature(mw_instance.pre, context_variables=context_variables)
            if not mw_instance.can_forward:
                logger.debug("{} pre returned error {}", mw_instance, mw_instance.error)
                return None

            mw_instances.append(mw_instance)

        return mw_instances

    async def post_middleware(
        self,
        mw_instances: List[BaseMiddleware],
        handle_responses: Optional[List] = None,
        handlers: Optional[List["ABCHandler"]] = None,
        context_variables: Optional[dict] = None,
    ):
        for middleware in mw_instances:
            # Update or leave value
            middleware.handle_responses = handle_responses or middleware.handle_responses
            middleware.handlers = handlers or middleware.handlers

            await call_by_signature(middleware.post, context_variables=context_variables)
            if not middleware.can_forward:
                logger.debug("{} post returned error {}", middleware, middleware.error)
                return middleware.error

    @abstractmethod
    async def handle_event(
        self,
        event: T_contra,
        ctx_api: "ABCAPI",
        state_dispenser: "ABCStateDispenser",
    ) -> None:
        pass

    def register_middleware(self, middleware: Type[BaseMiddleware]):
        try:
            if not issubclass(middleware, BaseMiddleware):
                raise ValueError("Argument is not a subclass of BaseMiddleware")
        except TypeError as e:
            raise ValueError("Argument is not a class") from e
        self.middlewares.append(middleware)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"handlers={self.handlers} "
            f"middlewares={self.middlewares} "
            f"handler_return_manager={self.handler_return_manager}"
        )
