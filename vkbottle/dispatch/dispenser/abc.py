from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from vkbottle_types import BaseStateGroup, StatePeer

from vkbottle.modules import logger


class ABCStateDispenser(ABC):
    @abstractmethod
    async def get(self, peer_id: int) -> Optional["StatePeer"]:
        pass

    @abstractmethod
    async def set(self, peer_id: int, state: "BaseStateGroup", **payload):
        pass

    @abstractmethod
    async def delete(self, peer_id: int):
        pass

    async def cast(self, peer_id: Optional[int]) -> Optional["StatePeer"]:
        if peer_id is None:
            return None

        logger.debug(f"Casting state for peer_id {peer_id}")
        return await self.get(peer_id)
