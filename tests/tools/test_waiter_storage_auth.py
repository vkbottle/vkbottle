import asyncio

import pytest

from vkbottle.tools import CtxStorage
from vkbottle.tools.auth import UserAuth
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


def test_ctx_storage_delete_missing_key_is_noop():
    storage = CtxStorage(force_reset=True)
    # Deleting a key that isn't there must not raise KeyError.
    storage.delete("nonexistent")


@pytest.mark.asyncio
async def test_get_token_spreads_extra_kwargs():
    sent: dict = {}

    class _HTTP:
        async def request_json(self, url, method="GET", data=None, **kw):
            sent.update(data or {})
            return {"access_token": "tok"}

    auth = UserAuth(client_id=1, client_secret="s")
    auth.http_client = _HTTP()

    result = await auth.get_token("login", "secret-pass", device_id="abc")

    assert result == "tok"
    # Extra kwargs must be spread as top-level POST fields, not nested under "kwargs".
    assert sent.get("device_id") == "abc"
    assert "kwargs" not in sent
