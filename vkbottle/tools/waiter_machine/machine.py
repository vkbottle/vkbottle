import asyncio
import typing
import datetime
import types

from vkbottle.dispatch.rules.abc import ABCRule
from vkbottle.dispatch.views.abc import ABCDispenseView

from .middleware import WaiterMiddleware
from .short_state import Behaviour, EventModel, ShortState

Identificator = typing.Union[str, int]
Storage = typing.Dict[str, typing.Dict[Identificator, "ShortState"]]


class WaiterMachine:
    def __init__(self) -> None:
        self.storage: Storage = {}
        self.middleware = WaiterMiddleware(self)

    async def drop(
        self,
        dispensable_view: ABCDispenseView[dict, EventModel],
        id: Identificator,
        **context,
    ) -> None:
        view_name = dispensable_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {} found".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if not short_state:
            raise LookupError(
                "Waiter with identificator {} is not found for view {}".format(id, view_name)
            )

        waiters: typing.Iterable[asyncio.Future] = short_state.event._waiters  # type: ignore

        for future in waiters:
            future.cancel()

        await self.call_behaviour(
            dispensable_view,  # type: ignore
            short_state.on_drop_behaviour,
            short_state.event,
            **context,
        )

    async def wait(
        self,
        dispensable_view: ABCDispenseView[dict, EventModel],
        linked_event: EventModel,
        *rules: ABCRule[EventModel],
        default: Behaviour = None,
        on_drop: Behaviour = None,
        expiration: typing.Union[datetime.timedelta, int, None] = None,
    ) -> typing.Tuple[EventModel, dict]:
        if isinstance(expiration, int):
            expiration = datetime.timedelta(seconds=expiration)

        event = asyncio.Event()

        key = dispensable_view.get_state_key(linked_event)
        if not key:
            msg = "Unable to get state key"
            raise RuntimeError(msg)

        short_state = ShortState(
            key,
            ctx_api=linked_event.ctx_api,  # type: ignore
            event=event,
            rules=rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
        )

        view_name = dispensable_view.__class__.__name__
        if view_name not in self.storage:
            dispensable_view.middlewares.append(self.middleware)  # type: ignore
            self.storage[view_name] = {}

        self.storage[view_name][key] = short_state

        await event.wait()

        e, ctx = getattr(event, "context")  # ruff: noqa
        self.storage[view_name].pop(key)

        return e, ctx

    async def call_behaviour(
        self,
        view: ABCDispenseView[dict, EventModel],
        behaviour: Behaviour,
        event: EventModel,
        **context,
    ) -> None:
        if behaviour is None:
            return
        value = behaviour
        if callable(behaviour):
            value = value(event)  # type: ignore
        if isinstance(value, types.CoroutineType):
            value = await value

        if return_handler := view.handler_return_manager.get_handler(value):
            await return_handler(
                view.handler_return_manager,
                value,
                event,
                context,
            )
