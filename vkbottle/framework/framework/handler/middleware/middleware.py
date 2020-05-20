from vkbottle.types import BaseModel
from enum import Enum, auto
from abc import ABC, abstractmethod
import warnings


class Middleware(ABC):
    async def pre(self, event: BaseModel):
        ...

    async def post(self, event: BaseModel):
        ...

    async def middleware(self, event: BaseModel):
        return MiddlewareFlags.UNASSIGNED

    async def emulate_middleware(self, event: BaseModel, flag: "MiddlewareFlags"):
        """ Emulate middleware based on given flag: PRE or POST
        :param event: Base executed event
        :param flag: MiddlewareFlags
        """
        deprecated_emul = await self.middleware(event)
        if deprecated_emul != MiddlewareFlags.UNASSIGNED:
            if flag is MiddlewareFlags.POST:
                return
            warnings.warn(
                "Middleware.middleware is deprecated, use pre and post instead. See issue #108"
            )
            return await self.middleware(event)

        elif flag is MiddlewareFlags.PRE:
            return await self.pre(event)

        elif flag is MiddlewareFlags.POST:
            return await self.post(event)

    def __repr__(self):
        return f"<Middleware {self.__class__.__qualname__}>"


class MiddlewareFlags(Enum):
    PRE = auto()
    POST = auto()
    UNASSIGNED = auto()
