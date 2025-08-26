import datetime
import typing

from vkbottle.dispatch.handlers.from_func_handler import FromFuncHandler
from vkbottle.dispatch.middlewares.abc import BaseMiddleware

if typing.TYPE_CHECKING:
    from .machine import WaiterMachine
    from .short_state import ShortState


class WaiterMiddleware(BaseMiddleware[dict]):
    def __init__(self, machine: "WaiterMachine") -> None:
        self.machine = machine

    def __call__(self, *args: typing.Any, **kw: typing.Any) -> "WaiterMiddleware":
        middleware = self.__class__(self.machine)
        super(WaiterMiddleware, middleware).__init__(*args, **kw)
        return middleware

    async def pre(self) -> None:
        if not self.view or not hasattr(self.view, "get_state_key"):
            msg = "WaiterMiddleware cannot be used inside a view which doesn't provide get_state_key (ABCDispenseView interface)"
            raise RuntimeError(msg)

        view_name = self.view.__class__.__name__
        if view_name not in self.machine.storage:
            return

        key = self.view.get_state_key(self.event)
        short_state: typing.Optional["ShortState"] = self.machine.storage[view_name].get(key)
        if not short_state:
            return

        if (
            short_state.expiration_date is not None
            and datetime.datetime.now() >= short_state.expiration_date
        ):
            await self.machine.drop(self.view, short_state.key)  # type: ignore
            return

        context = {}
        if short_state.context is not None:
            context.update(short_state.context.context)

        if short_state.exit_behaviour is not None and await self.machine.call_behaviour(
            self.view,  # type: ignore
            short_state.exit_behaviour,
            self.event,
            **context,
        ):
            await self.machine.drop(self.view, short_state.key)  # type: ignore
            return

        handler: FromFuncHandler = FromFuncHandler(self.pass_runtime, *short_state.rules)
        result = await handler.filter(self.event, context)

        if result is not False:
            if isinstance(result, bool):
                result = {}
            result.update(context)
            context.setdefault("short_state", short_state)
            await handler.handle(self.event, **context)

        elif short_state.default_behaviour is not None:
            await self.machine.call_behaviour(
                self.view,  # type: ignore
                short_state.default_behaviour,
                self.event,
                **context,
            )

        self.stop("Runtime was passed to waiter.")

    async def pass_runtime(
        self,
        event: typing.Any,
        short_state: "ShortState[dict]",
        **context: typing.Any,
    ) -> None:
        short_state.context = (event, context)  # type: ignore
        short_state.event.set()


__all__ = ("WaiterMiddleware",)
