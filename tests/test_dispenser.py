import pytest

from vkbottle.dispatch.dispenser.base import StateRepresentation
from vkbottle.dispatch.dispenser.builtin import BuiltinStateDispenser


@pytest.mark.asyncio
async def test_dispenser_delete_unknown_peer_is_noop():
    dispenser = BuiltinStateDispenser()
    # Deleting a peer with no stored state must not raise (drop() already tolerates it).
    await dispenser.delete(404)


def test_state_representation_is_hashable():
    state = StateRepresentation("Foo:bar")
    # Overriding __eq__ without __hash__ would make StateRepresentation unhashable,
    # which in turn breaks hashing wherever a state representation is used.
    assert hash(state) == hash("Foo:bar")
    # Hash + equality are consistent, so it dedups against the equal plain string.
    assert {state, "Foo:bar"} == {"Foo:bar"}
