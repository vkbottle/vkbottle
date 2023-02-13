import asyncio
import typing
from abc import ABC

import aioredis
from .abc import ABCStateDispenser, BaseStateGroup, StatePeer
from vkbottle.dispatch.dispenser import get_state_repr

STATE_KEY = 'state'
STATE_DATA_KEY = 'data'


class RedisDispenser(ABCStateDispenser):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: typing.Optional[int] = None,
            password: typing.Optional[str] = None,
            ssl: typing.Optional[bool] = None,
            pool_size: int = 10,
            loop: typing.Optional[asyncio.AbstractEventLoop] = None,
            prefix: str = "fsm",
            state_ttl: typing.Optional[int] = None,
            data_ttl: typing.Optional[int] = None,
            bucket_ttl: typing.Optional[int] = None,
            **kwargs,
    ):
        self._redis = aioredis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            ssl=ssl,
            max_connections=pool_size,
            decode_responses=True,
            **kwargs,
        )
        self._prefix = (prefix,)

    def generate_key(self, *parts):
        return ':'.join(self._prefix + tuple(map(str, parts)))

    async def get(self, peer_id: int) -> typing.Optional[StatePeer]:
        key_ = self.generate_key(peer_id, STATE_KEY)
        val = await self._redis.get(key_)

        if not val:
            return None

        payload_key_ = self.generate_key(peer_id, STATE_DATA_KEY)
        user_payload = await self._redis.hgetall(payload_key_)

        return StatePeer(peer_id=peer_id, state=val, payload=user_payload)

    async def set(self, peer_id: int, state: BaseStateGroup, **payload):
        key_ = self.generate_key(peer_id, STATE_KEY)
        await self._redis.set(key_, get_state_repr(state))

        if payload:
            payload_key_ = self.generate_key(peer_id, STATE_DATA_KEY)
            await self._redis.hmset(payload_key_, payload)

    async def delete(self, peer_id: int):
        key_ = self.generate_key(peer_id, STATE_KEY)
        await self._redis.delete(key_)
