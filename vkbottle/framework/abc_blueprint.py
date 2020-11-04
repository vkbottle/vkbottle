from .abc import ABCFramework
from vkbottle.api import ABCAPI
from vkbottle.polling import ABCPolling
from vkbottle.dispatch import ABCRouter
from typing import Optional, NoReturn, Any
from abc import abstractmethod

import asyncio


class ABCBlueprint(ABCFramework):
    router: ABCRouter

    _polling: Optional[ABCPolling] = None
    _api: Optional[ABCAPI] = None

    name: str = "Unnamed"
    constructed: bool = False

    @abstractmethod
    def construct(self, api: ABCAPI, polling: ABCPolling) -> "ABCBlueprint":
        pass

    @abstractmethod
    def load(self, framework: Any) -> "ABCBlueprint":
        pass

    @property
    def polling(self) -> ABCPolling:
        if not self._polling:
            raise RuntimeError("You need to construct blueprint firstly")
        return self._polling

    @polling.setter
    def polling(self, new_polling: ABCPolling):  # type: ignore
        self._polling = new_polling

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_running_loop()

    @property  # type: ignore
    def api(self) -> ABCAPI:  # type: ignore
        if not self._api:
            raise RuntimeError(
                "You need to construct blueprint firstly. "
                "Beware: if you use multibot, api can only be accessed with event.ctx_api"
            )
        return self._api

    @api.setter
    def api(self, new_api: ABCAPI):
        self._api = new_api

    async def run_polling(self) -> NoReturn:
        raise RuntimeError("You are not allowed to run polling with blueprint")

    def run_forever(self) -> NoReturn:
        raise RuntimeError("You are not allowed to run polling with blueprint")

    def __repr__(self):
        return f"<Blueprint {self.name!r} {self.__class__.__qualname__} constructed={self.constructed}>"
