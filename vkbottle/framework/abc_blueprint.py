import asyncio
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, NoReturn, Optional, Union

from .abc import ABCFramework

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.dispatch import ABCRouter, ABCStateDispenser
    from vkbottle.polling import ABCPolling

CONSTRUCT_BLUEPRINT = "You need to construct blueprint firstly"


class ABCBlueprint(ABCFramework):
    router: "ABCRouter"

    _polling: "ABCPolling"
    _api: "ABCAPI"
    _state_dispenser: "ABCStateDispenser"

    name: str = "Unnamed"
    constructed: bool = False

    @abstractmethod
    def construct(
        self, api: "ABCAPI", polling: "ABCPolling", state_dispenser: "ABCStateDispenser"
    ) -> "ABCBlueprint":
        pass

    @abstractmethod
    def load(self, framework: Any) -> "ABCBlueprint":
        pass

    @property
    def polling(self) -> "ABCPolling":
        self.assert_constructed()
        return self._polling

    @polling.setter
    def polling(self, new_polling: "ABCPolling"):  # type: ignore
        self._polling = new_polling

    @property
    def state_dispenser(self) -> "ABCStateDispenser":
        self.assert_constructed()
        return self._state_dispenser

    @state_dispenser.setter
    def state_dispenser(self, new_state_dispenser: "ABCStateDispenser"):
        self._state_dispenser = new_state_dispenser

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_running_loop()

    @property  # type: ignore
    def api(self) -> Union["ABCAPI", "API"]:  # type: ignore
        if not self._api:
            raise RuntimeError(
                CONSTRUCT_BLUEPRINT
                + " Beware: if you use multibot, api can only be accessed with event.ctx_api"
            )
        return self._api

    @api.setter
    def api(self, new_api: "ABCAPI"):
        self._api = new_api

    async def run_polling(self) -> NoReturn:
        raise RuntimeError("You are not allowed to run polling with blueprint")

    def run_forever(self) -> NoReturn:
        raise RuntimeError("You are not allowed to run polling with blueprint")

    def assert_constructed(self) -> Optional[NoReturn]:
        if not self.constructed:
            raise RuntimeError(CONSTRUCT_BLUEPRINT)

    def __repr__(self):
        return f"<Blueprint {self.name!r} {self.__class__.__qualname__} constructed={self.constructed}>"
