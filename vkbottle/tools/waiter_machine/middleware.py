import typing

from vkbottle.dispatch.dispenser.builtin import BuiltinStateDispenser
from vkbottle.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle.dispatch.middlewares.abc import BaseMiddleware

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine
    from .short_state import ShortState


class WaiterMiddleware(BaseMiddleware[dict]):
    def __init__(
        self,
        machine: "WaiterMachine",
    ) -> None:
        self.machine = machine
        self.state_dispenser = BuiltinStateDispenser()

    def __call__(self, *args, **kw) -> "WaiterMiddleware":
        middleware = self.__class__(self.machine)
        super(WaiterMiddleware, middleware).__init__(*args, **kw)
        return middleware

    async def pre(self) -> None:
        if not self.view or not hasattr(self.view, "get_state_key"):
            msg = "WaiterMiddleware cannot be used inside a view which doesn't provide get_state_key (ABCDispenseView Protocol)"
            raise RuntimeError(msg)

        view_name = self.view.__class__.__name__
        if view_name not in self.machine.storage:
            return

        key = self.view.get_state_key(self.event)
        short_state: typing.Optional["ShortState"] = self.machine.storage[view_name].get(key)
        if not short_state:
            return

        handler: FromFuncHandler = FromFuncHandler(self.pass_runtime, *short_state.rules)

        result = await handler.filter(self.event)

        if result is not False:
            if isinstance(result, bool):
                result = {}
            await handler.handle(self.event, short_state=short_state, **result)
        elif short_state.default_behaviour is not None:
            value = short_state.default_behaviour
            if callable(value):
                value = value(self.event)

            if return_handler := self.view.handler_return_manager.get_handler(value):
                await return_handler(
                    self.view.handler_return_manager,
                    value,
                    self.event,
                    result,
                )

        self.stop("Runtime was passed to waiter")

    async def pass_runtime(self, event, short_state: "ShortState", **context) -> None:
        setattr(short_state.event, "context", (event, context))  # ruff: noqa
        short_state.event.set()
