from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
    from vkbottle.dispatch.handlers import ABCHandler
    from vkbottle.dispatch.return_manager import BaseReturnManager
    from vkbottle.exception_factory import ABCErrorHandler

    Handlers = list["ABCHandler[Any]"] | dict[Any, list[Any]]

T_contra = TypeVar("T_contra", list, dict, contravariant=True)


class ABCView(ABC, Generic[T_contra]):
    handlers: "Handlers"
    middlewares: list[type["BaseMiddleware[T_contra]"]]
    handler_return_manager: "BaseReturnManager"
    _error_handler: "ABCErrorHandler | None"

    @abstractmethod
    def __init__(self, error_handler: "ABCErrorHandler | None" = None) -> None:
        self.handlers = []
        self.middlewares = []
        self.handler_return_manager = None  # type: ignore
        self._error_handler = error_handler

    @property
    def error_handler(self) -> "ABCErrorHandler":
        if self._error_handler is None:
            from vkbottle.exception_factory.error_handler import ErrorHandler

            self._error_handler = ErrorHandler()

        return self._error_handler

    @error_handler.setter
    def error_handler(self, error_handler: "ABCErrorHandler") -> None:
        self._error_handler = error_handler

    @abstractmethod
    async def process_event(self, event: T_contra) -> bool:
        pass

    async def pre_middleware(
        self,
        event: T_contra,
        context_variables: dict[str, Any] | None = None,
    ) -> list[BaseMiddleware[T_contra]] | None:
        """Run all of the pre middleware methods and return an exception if any error occurs"""
        mw_instances = []

        for middleware in self.middlewares:
            mw_instance = middleware(event, view=self)

            await mw_instance.pre()

            if not mw_instance.can_forward:
                logger.debug("{} pre returned error: {}", mw_instance, mw_instance.format_error())
                return None

            mw_instances.append(mw_instance)

            if context_variables is not None:
                context_variables.update(mw_instance.context_update)

        return mw_instances

    async def post_middleware(
        self,
        mw_instances: list[BaseMiddleware[T_contra]],
        handle_responses: list[Any] | None = None,
        handlers: list["ABCHandler[Any]"] | None = None,
    ) -> Exception | None:
        for middleware in mw_instances:
            # Update or leave value
            middleware.handle_responses = handle_responses or middleware.handle_responses
            middleware.handlers = handlers or middleware.handlers

            await middleware.post()

            if not middleware.can_forward:
                logger.debug("{} post returned error: {}", middleware, middleware.format_error())
                return middleware.error

    @abstractmethod
    async def handle_event(
        self,
        event: T_contra,
        ctx_api: "ABCAPI",
        state_dispenser: "ABCStateDispenser",
    ) -> None:
        pass

    def register_middleware(self, middleware: type[BaseMiddleware]) -> None:
        try:
            if not issubclass(middleware, BaseMiddleware):
                msg = "Argument is not a subclass of BaseMiddleware"
                raise ValueError(msg)
        except TypeError as e:
            msg = "Argument is not a class"
            raise ValueError(msg) from e

        self.middlewares.append(middleware)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"handlers={self.handlers!r} "
            f"middlewares={self.middlewares!r} "
            f"handler_return_manager={self.handler_return_manager!r}"
        )


__all__ = ("ABCView",)
