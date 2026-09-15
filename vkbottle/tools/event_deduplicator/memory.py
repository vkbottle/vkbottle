import asyncio
import hashlib
import json
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, Final, Mapping

from typing_extensions import override

from .abc import ABCEventDeduplicator

# MemoryEventDeduplicator
# ttl 300, max_size 10_000
# Event received -> call claim(event) -> generate _keys (first key - payload, second - event_id:{group_id}:{event_id})
# -> block (async with _lock) -> Clear old ttl -> if have key -> return False (it's duplicate)
# -> if not have key -> add keys to cache with current time -> check cache size -> if size > max_size -> remove oldest (FIFO)
# -> return True (new event)

_PAYLOAD_FIELDS: Final = ("type", "object", "group_id")
_IDENTITY_WRAPPERS: Final = ("message",)
_IDENTITY_FIELDS: Final = (
    "id",
    "owner_id",
    "peer_id",
    "conversation_message_id",
    "from_id",
    "to_id",
    "user_id",
    "liker_id",
    "deleter_id",
    "admin_id",
    "post_id",
    "photo_id",
    "video_id",
    "item_id",
    "topic_id",
    "poll_id",
    "option_id",
    "object_id",
    "object_type",
    "object_owner_id",
    "date",
    "update_time",
    "random_id",
)
_SCALARS: Final = (int, str)


class MemoryEventDeduplicator(ABCEventDeduplicator):
    def __init__(
        self,
        ttl: float = 300.0,
        max_size: int = 10_000,
        *,
        timer: Callable[[], float] = time.monotonic,
    ) -> None:
        if ttl <= 0:
            msg = "Event deduplication TTL must be greater than zero"
            raise ValueError(msg)

        if max_size <= 0:
            msg = "Event deduplication cache size must be greater than zero"
            raise ValueError(msg)

        self.ttl = ttl
        self.max_size = max_size
        self._timer = timer
        self._claims: OrderedDict[int, tuple[float, tuple[str, ...]]] = OrderedDict()
        self._keys_index: dict[str, int] = {}
        self._next_claim_id = 0
        self._lock = asyncio.Lock()

    def __len__(self) -> int:
        return len(self._claims)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({len(self)} claims) ttl={self.ttl}, max_size={self.max_size}>"

    @staticmethod
    def _digest(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    @staticmethod
    def _identity(event: Mapping[str, Any]) -> tuple[Any, ...] | None:
        event_type = event.get("type")

        if not isinstance(event_type, str):
            return None

        node = event.get("object")

        if not isinstance(node, dict):
            return None

        for wrapper in _IDENTITY_WRAPPERS:
            nested = node.get(wrapper)

            if isinstance(nested, dict):
                node = nested
                break

        values: tuple[Any, ...] = tuple(
            (field, node[field]) for field in _IDENTITY_FIELDS if type(node.get(field)) in _SCALARS
        )
        return None if not values else (event_type, event.get("group_id"), values)

    @classmethod
    def _keys(cls, event: Mapping[str, Any]) -> tuple[str, ...]:
        keys: list[str] = []

        identity = cls._identity(event)

        if identity is not None:
            keys.append(f"identity:{cls._digest(repr(identity))}")
        else:
            payload = {field: event[field] for field in _PAYLOAD_FIELDS if field in event}

            if payload:
                serialized = json.dumps(
                    payload,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                keys.append(f"payload:{cls._digest(serialized)}")

        event_id = event.get("event_id")
        if event_id is not None:
            keys.append(f"event_id:{cls._digest(repr((event.get('group_id'), event_id)))}")

        return tuple(keys)

    def _drop(self, claim_id: int) -> None:
        _claimed_at, keys = self._claims.pop(claim_id)
        for key in keys:
            self._keys_index.pop(key, None)

    def _sweep(self, now: float) -> None:
        expired_before = now - self.ttl

        while self._claims:
            claim_id, (claimed_at, _keys) = next(iter(self._claims.items()))

            if claimed_at > expired_before:
                break

            self._drop(claim_id)

    @override
    async def claim(self, event: Mapping[str, Any]) -> bool:
        keys = self._keys(event)
        if not keys:
            return True

        async with self._lock:
            now = self._timer()
            self._sweep(now)

            if any(key in self._keys_index for key in keys):
                return False

            claim_id = self._next_claim_id
            self._next_claim_id += 1
            self._claims[claim_id] = (now, keys)

            for key in keys:
                self._keys_index[key] = claim_id

            while len(self._claims) > self.max_size:
                self._drop(next(iter(self._claims)))

            return True

    async def release(self, event: Mapping[str, Any]) -> None:
        keys = self._keys(event)
        if not keys:
            return

        async with self._lock:
            for key in keys:
                claim_id = self._keys_index.get(key)

                if claim_id is not None:
                    self._drop(claim_id)

    async def clear(self) -> None:
        async with self._lock:
            self._claims.clear()
            self._keys_index.clear()


__all__ = ("MemoryEventDeduplicator",)
