from copy import copy
from vkbottle.utils import logger
import typing

from vkbottle.types.message import Message


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

    async def enter(self):
        ...

    async def branch(self, ans: Message, *args):
        ...

    async def exit(self):
        ...

    def __repr__(self):
        return f"<Branch {self.__class__.__name__}>"


class ClsBranch(AbstractBranch):
    async def enter(self):
        logger.info("Branch {} entered at", self.key)

    async def exit(self):
        logger.info("Branch {} exit at", self.key)


class CoroutineBranch(AbstractBranch):
    async def enter(self):
        logger.info("Branch {} entered at", self.key or self.data["call"].__name__)

    async def exit(self):
        logger.info("Branch {} exit at", self.key or self.data["call"].__name__)

    async def branch(self, ans, *args):
        return await self.data["call"](ans, *args, **self.context)

    def __call__(self):
        return self
