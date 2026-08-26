import asyncio
import hashlib
from collections import OrderedDict
from typing import Any, Final, Mapping

from vkbottle_types.base_model import PYDICT_APAPTER_TO_RAW_JSON

from vkbottle.tools.limited_dict import LimitedDict

from .abc import ABCEventDeduplicator

KEYS: Final[tuple[str, ...]] = tuple(sorted(("type", "group_id", "object")))

# MemoryEventDeduplicator
# ttl 300, max_size 10_000
# Event received -> call claim(event) -> generate _keys (first key - payload, second - event_id:{group_id}:{event_id})
# -> block (async with _lock) -> Clear old ttl -> if have key -> return False (it's duplicate)
# -> if not have key -> add keys to cache with current time -> check cache size -> if size > max_size -> remove oldest (FIFO)
# -> return True (new event)


class MemoryEventDeduplicator(ABCEventDeduplicator):
    def __init__(self, ttl: float = 300.0, max_size: int = 10_000) -> None:
        if ttl <= 0:
            msg = "Event deduplication TTL must be greater than zero"
            raise ValueError(msg)

        if max_size <= 0:
            msg = "Event deduplication cache size must be greater than zero"
            raise ValueError(msg)

        self._ttl = ttl
        self._claims = LimitedDict(
            maxlimit=max_size,
            dict_factory=OrderedDict[str, float],
        )
        self._lock = asyncio.Lock()

    @staticmethod
    def _keys(event: Mapping[str, Any]) -> tuple[str, ...]:
        serialized = PYDICT_APAPTER_TO_RAW_JSON.dump_json(
            {key: event[key] for key in KEYS if key in event},
            ensure_ascii=False,
            fallback=str,
        )
        fingerprint = hashlib.sha256(serialized).hexdigest()
        keys: tuple[str, ...] = (f"payload:{fingerprint}",)

        event_id = event.get("event_id")
        if event_id is not None:
            keys += (f"event_id:{event.get('group_id')}:{event_id}",)

        return keys

    async def claim(self, event: Mapping[str, Any]) -> bool:
        async with self._lock:
            now = asyncio.get_running_loop().time()
            expired_before = now - self._ttl

            while self._claims:
                oldest = self._claims.get_oldest_pair()
                if oldest is None:
                    break

                key, expires = oldest
                if expires > expired_before:
                    break

                del self._claims[key]

            keys = self._keys(event)

            if any(key in self._claims for key in keys):
                return False

            for key in keys:
                self._claims.set(key, now)

            return True


__all__ = ("MemoryEventDeduplicator",)
