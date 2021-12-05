from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Dict, Type

if TYPE_CHECKING:
    from vkbottle.api.abc import ABCAPI
    from vkbottle.exception_factory.error_handler import ABCErrorHandler

    from .dispenser.abc import ABCStateDispenser
    from .views import ABCView


class ABCRouter(ABC):
    """Abstract Router
    Documentation: soon
    """

    views: Dict[str, "ABCView"] = {}
    state_dispenser: "ABCStateDispenser"
    error_handler: "ABCErrorHandler"

    @abstractmethod
    async def route(self, event: dict, ctx_api: "ABCAPI") -> None:
        pass

    @abstractmethod
    def construct(
        self,
        views: Dict[str, "ABCView"],
        state_dispenser: "ABCStateDispenser",
        error_handler: "ABCErrorHandler",
    ) -> "ABCRouter":
        pass

    def add_view(self, name: str, view: "ABCView") -> None:
        self.views[name] = view

    def view(self, name: str) -> Callable[..., Type["ABCView"]]:
        def decorator(view: Type["ABCView"]):
            self.add_view(name, view())
            return view

        return decorator
