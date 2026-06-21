import pytest

from vkbottle.dispatch.dispenser.builtin import BuiltinStateDispenser


@pytest.mark.asyncio
async def test_dispenser_delete_unknown_peer_is_noop():
    dispenser = BuiltinStateDispenser()
    # Deleting a peer with no stored state must not raise (drop() already tolerates it).
    await dispenser.delete(404)
