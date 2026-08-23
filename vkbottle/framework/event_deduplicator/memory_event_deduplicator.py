import asyncio
import hashlib
import json
import time
from collections import OrderedDict
from typing import Any

from .abc import ABCEventDeduplicator

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

        self.ttl = ttl
        self.max_size = max_size
        self._claims: OrderedDict[str, float] = OrderedDict()
        self._lock = asyncio.Lock()

    @staticmethod
    def _keys(event: dict[str, Any]) -> tuple[str, ...]:
        payload = {key: event[key] for key in ("type", "object", "group_id") if key in event}
        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        fingerprint = hashlib.sha256(serialized.encode()).hexdigest()
        keys = [f"payload:{fingerprint}"]

        event_id = event.get("event_id")
        if event_id is not None:
            keys.append(f"event_id:{event.get('group_id')}:{event_id}")
        return tuple(keys)

    async def claim(self, event: dict[str, Any]) -> bool:
        now = time.monotonic()
        keys = self._keys(event)

        async with self._lock:
            expired_before = now - self.ttl
            while self._claims and next(iter(self._claims.values())) <= expired_before:
                self._claims.popitem(last=False)

            if any(key in self._claims for key in keys):
                return False

            for key in keys:
                self._claims[key] = now
            while len(self._claims) > self.max_size:
                self._claims.popitem(last=False)
            return True


__all__ = ("MemoryEventDeduplicator",)
