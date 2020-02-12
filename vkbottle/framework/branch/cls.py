from copy import copy
from ...utils import logger

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

    async def branch(self, ans: Message):
        ...

    async def exit(self, ans: Message):
        ...


class ClsBranch(AbstractBranch):
    async def enter(self, ans: Message):
        logger.info("Branch {} entered at", self.key)

    async def exit(self, ans: Message):
        logger.info("Branch {} exit at", self.key)


class FunctionBranch(ClsBranch):
    async def branch(self, ans: Message):
        return await self.data["call"](ans, **self.context)
