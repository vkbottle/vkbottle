from .abc import ABCStateDispenser
from vkbottle_types import StatePeer, BaseStateGroup
from typing import Optional, Dict


class BuiltinStateDispenser(ABCStateDispenser):
    def __init__(self):
        self.dictionary: Dict[int, StatePeer] = {}

    async def get(self, peer_id: int) -> Optional[StatePeer]:
        return self.dictionary.get(peer_id)

    async def set(self, peer_id: int, state: BaseStateGroup):
        self.dictionary[peer_id] = StatePeer(peer_id=peer_id, state=state)

    async def delete(self, peer_id: int):
        self.dictionary.pop(peer_id)
