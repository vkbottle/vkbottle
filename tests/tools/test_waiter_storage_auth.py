import asyncio

import pytest

from vkbottle.tools.waiter_machine.machine import WaiterMachine


class _View:
    def __init__(self) -> None:
        self.middlewares: list = []

    def get_state_key(self, event) -> str:
        return "key1"


class _Event:
    ctx_api = None


@pytest.mark.asyncio
async def test_waiter_wait_tolerates_key_removed_during_wait():
    machine = WaiterMachine()
    view = _View()

    wait_task = asyncio.create_task(machine.wait(view, _Event()))
    await asyncio.sleep(0)  # let wait() set up and park on event.wait()

    view_name = type(view).__name__
    short_state = machine.storage[view_name]["key1"]
    short_state.context = object()  # pretend a matching event filled the context

    # A concurrent drop/eviction removes the key, then the waiter is released.
    machine.storage[view_name].pop("key1", None)
    short_state.event.set()

    # wait() must not KeyError on the already-removed key.
    result = await wait_task
    assert result is short_state.context
