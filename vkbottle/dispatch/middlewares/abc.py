from abc import ABC


class BaseMiddleware(ABC):
    async def pre(self, event):
        ...

    async def post(self, event, view):
        ...
