from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

from typing_extensions import Self

if TYPE_CHECKING:
    from vkbottle.api.abc import ABCAPI
    from vkbottle.exception_factory.error_handler import ABCErrorHandler

    from .dispenser.abc import ABCStateDispenser
    from .views import ABCView


class ABCRouter(ABC):
    """Abstract Router
    Documentation: https://vkbottle.rtfd.io/ru/latest/high-level/handling/router/
    """

    views: dict[str, "ABCView"]
    state_dispenser: "ABCStateDispenser"
    error_handler: "ABCErrorHandler"

    def __init__(self) -> None:
        self.views = {}

    @abstractmethod
    async def route(self, event: dict[str, Any], ctx_api: "ABCAPI") -> None:
        pass

    @abstractmethod
    def construct(
        self,
        views: dict[str, "ABCView"],
        state_dispenser: "ABCStateDispenser",
        error_handler: "ABCErrorHandler",
    ) -> Self:
        pass

    def add_view(self, name: str, view: "ABCView") -> None:
        self.views[name] = view

    def view(self, name: str) -> Callable[..., type["ABCView"]]:
        def decorator(view: type["ABCView"]):
            self.add_view(name, view())
            return view

        return decorator


__all__ = ("ABCRouter",)
