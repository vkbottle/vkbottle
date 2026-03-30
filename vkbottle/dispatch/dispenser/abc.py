from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from vkbottle.modules import logger

if TYPE_CHECKING:
    from .base import BaseStateGroup, StatePeer


class ABCStateDispenser(ABC):
    @abstractmethod
    async def get(self, peer_id: int) -> "StatePeer | None":
        pass

    @abstractmethod
    async def set(self, peer_id: int, state: "BaseStateGroup", **payload):
        pass

    @abstractmethod
    async def delete(self, peer_id: int):
        pass

    async def cast(self, peer_id: int | None) -> "StatePeer | None":
        if peer_id is None:
            return None

        logger.debug("Casting state for peer_id {}", peer_id)
        return await self.get(peer_id)
