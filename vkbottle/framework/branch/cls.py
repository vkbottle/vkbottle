from copy import copy
from ...utils import logger
import typing

from ...types import Message


class Copy:
    def copy(self):
        return copy(self)


class AbstractBranch(Copy):
    def __init__(self, name: str = None, **kwargs):
        if not hasattr(self, "key"):
            self.key = name if name is not None else getattr(self, "__class__").__name__
        self.data = kwargs

    def create(self, **context):
        self.context = context
        ...

    async def enter(self, ans: Message):
        ...

    async def branch(self, ans: Message, *args):
        ...

    async def exit(self, ans: Message):
        ...


class ClsBranch(AbstractBranch):
    async def enter(self, ans: Message):
        logger.info("Branch {} entered at", self.key)

    async def exit(self, ans: Message):
        logger.info("Branch {} exit at", self.key)


class CoroutineBranch(AbstractBranch):
    async def enter(self, ans):
        logger.info("Branch {} entered at", self.key or self.data["call"].__name__)

    async def exit(self, ans):
        logger.info("Branch {} exit at", self.key or self.data["call"].__name__)

    async def branch(self, ans, *args):
        return await self.data["call"](ans, *args)
