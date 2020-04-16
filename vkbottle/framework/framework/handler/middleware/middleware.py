from vkbottle.types import BaseModel


class Middleware:
    async def middleware(self, event: BaseModel):
        ...

    async def __call__(self, *args, **kwargs):
        return await self.middleware(*args, **kwargs)

    def __repr__(self):
        return f"<Middleware {self.__class__.__qualname__}>"
