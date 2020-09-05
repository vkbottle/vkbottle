from .abc import ABCFramework
from vkbottle.api import ABCAPI, API
from vkbottle.polling import ABCPolling, BotPolling
from vkbottle.tools import LoopWrapper
from vkbottle.dispatch import ABCRouter, BotRouter
from asyncio import AbstractEventLoop, get_event_loop
from typing import Optional


class Bot(ABCFramework):
    def __init__(
        self,
        token: Optional[str] = None,
        api: Optional[ABCAPI] = None,
        polling: Optional[ABCPolling] = None,
        loop: Optional[AbstractEventLoop] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
    ):
        self.api = API(token) if token is not None else api
        self.loop_wrapper = loop_wrapper or LoopWrapper()
        self.router = router or BotRouter()
        self._polling = polling or BotPolling(self.api)
        self._loop = loop

    @property
    def polling(self) -> "ABCPolling":
        return self._polling.construct(self.api)  # type: ignore

    async def run_polling(self):
        async for event in self.polling.listen():
            for update in event["updates"]:
                await self.router.route(update)

    @property
    def loop(self) -> AbstractEventLoop:
        if self._loop is None:
            self._loop = get_event_loop()
        return self._loop

    @loop.setter
    def loop(self, new_loop: AbstractEventLoop):
        self._loop = new_loop

    def run_forever(self):
        self.loop_wrapper.add_task(self.run_polling())
        self.loop_wrapper.run_forever(self.loop)
