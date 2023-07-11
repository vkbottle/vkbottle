import asyncio
import typing

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

    async def wait(
        self,
        dispensable_view: ABCDispenseView[dict, EventModel],
        linked_event: EventModel,
        *rules: ABCRule[EventModel],
        default_behaviour: Behaviour = None,
    ) -> typing.Tuple[EventModel, dict]:
        event = asyncio.Event()
        short_state = ShortState(
            linked_event.ctx_api,  # type: ignore
            event,
            rules,
            default_behaviour,
        )

        key = dispensable_view.get_state_key(linked_event)
        if not key:
            msg = "Unable to get state key"
            raise RuntimeError(msg)

        view_name = dispensable_view.__class__.__name__
        if view_name not in self.storage:
            dispensable_view.middlewares.append(self.middleware)  # type: ignore
            self.storage[view_name] = {}

        self.storage[view_name][key] = short_state

        await event.wait()

        e, ctx = getattr(event, "context")  # ruff: noqa
        self.storage[view_name].pop(key)

        return e, ctx
