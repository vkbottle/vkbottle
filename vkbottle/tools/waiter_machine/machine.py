import asyncio
import datetime
import typing

from vkbottle.dispatch.rules.abc import ABCRule
from vkbottle.dispatch.views.abc import ABCDispenseView
from vkbottle.tools.limited_dict import LimitedDict

from .middleware import WaiterMiddleware
from .short_state import Behaviour, Event, ShortState

Identificator = typing.Union[str, int]
Storage = typing.Dict[str, LimitedDict[Identificator, "ShortState[Event]"]]


class WaiterMachine:
    def __init__(self, *, max_storage_size: int = 1000) -> None:
        self.storage: Storage = {}
        self.max_storage_size = max_storage_size
        self.middleware = WaiterMiddleware(self)

    async def drop(
        self,
        dispensable_view: ABCDispenseView[dict, Event],
        identifier: Identificator,
        **context: typing.Any,
    ) -> None:
        view_name = dispensable_view.__class__.__name__
        if view_name not in self.storage:
            msg = f"No record of view {view_name} found"
            raise LookupError(msg)

        short_state = self.storage[view_name].pop(identifier, None)
        if not short_state:
            msg = f"Waiter with identificator {identifier} is not found for view {view_name}"
            raise LookupError(msg)

        if short_state.context is not None:
            context.update(short_state.context.context)

        short_state.cancel()
        await self.call_behaviour(
            dispensable_view,  # type: ignore
            short_state.on_drop_behaviour,
            short_state.event,  # type: ignore
            **context,
        )

    async def wait(
        self,
        dispensable_view: ABCDispenseView[dict, Event],
        linked_event: Event,
        *rules: ABCRule[Event],
        default: Behaviour[Event] = None,
        on_drop: Behaviour[Event] = None,
        exit: Behaviour[Event] = None,  # noqa: A002
        expiration: typing.Union[datetime.timedelta, float, None] = None,
    ):
        if isinstance(expiration, (int, float)):
            expiration = datetime.timedelta(seconds=expiration)

        key = dispensable_view.get_state_key(linked_event)
        if not key:
            msg = "Unable to get state key."
            raise RuntimeError(msg)

        event = asyncio.Event()
        short_state = ShortState(
            key,
            ctx_api=linked_event.ctx_api,  # type: ignore
            event=event,
            rules=rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
            exit_behaviour=exit,
        )

        view_name = dispensable_view.__class__.__name__
        if view_name not in self.storage:
            dispensable_view.middlewares.insert(0, self.middleware)  # type: ignore
            self.storage[view_name] = LimitedDict(maxlimit=self.max_storage_size)

        if (deleted_short_state := self.storage[view_name].set(key, short_state)) is not None:
            deleted_short_state.cancel()

        self.storage[view_name][key] = short_state
        await event.wait()
        self.storage[view_name].pop(key)

        if short_state.context is None:
            msg = "Context is not defined."
            raise RuntimeError(msg)

        return short_state.context

    async def call_behaviour(
        self,
        view: ABCDispenseView[dict, Event],
        behaviour: Behaviour[Event],
        event: Event,
        **context: typing.Any,
    ) -> bool:
        if behaviour is None:
            return False

        result = await behaviour.filter(event, context)
        if result is not False:
            result = result if isinstance(result, dict) else {}
            context.update(result)
            value = await behaviour.handle(event, **context)
            if return_handler := view.handler_return_manager.get_handler(value):
                await return_handler(
                    view.handler_return_manager,
                    value,
                    event,
                    context,
                )
            return True

        return False


__all__ = ("WaiterMachine",)
