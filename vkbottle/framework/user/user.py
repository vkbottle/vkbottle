import asyncio
from typing import TYPE_CHECKING, Any, Optional, Type

from vkbottle.api import API
from vkbottle.dispatch import BuiltinStateDispenser, Router
from vkbottle.exception_factory import ErrorHandler
from vkbottle.framework.base import BaseFramework
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger
from vkbottle.polling import UserPolling
from vkbottle.tools import LoopWrapper, UserAuth

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, Token
    from vkbottle.dispatch import ABCRouter, ABCStateDispenser
    from vkbottle.exception_factory import ABCErrorHandler
    from vkbottle.framework.labeler import ABCLabeler
    from vkbottle.polling import ABCPolling


class User(BaseFramework):
    def __init__(
        self,
        token: Optional["Token"] = None,
        api: Optional["ABCAPI"] = None,
        polling: Optional["ABCPolling"] = None,
        loop_wrapper: Optional[LoopWrapper] = None,
        router: Optional["ABCRouter"] = None,
        labeler: Optional["ABCLabeler"] = None,
        state_dispenser: Optional["ABCStateDispenser"] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
        task_each_event=None,
    ) -> None:
        self.api: API = api or API(token)  # type: ignore
        self.error_handler = error_handler or ErrorHandler()
        self.loop_wrapper = loop_wrapper or LoopWrapper()
        self.labeler = labeler or UserLabeler()
        self.state_dispenser = state_dispenser or BuiltinStateDispenser()
        self._polling = polling or UserPolling(self.api)
        self._router = router or Router()

        if task_each_event:
            logger.warning("task_each_event is deprecated and will be removed in future versions")

    @property
    def polling(self) -> "ABCPolling":
        return self._polling.construct(self.api, self.error_handler)

    @property
    def router(self) -> "ABCRouter":
        return self._router.construct(
            views=self.labeler.views(),
            state_dispenser=self.state_dispenser,
            error_handler=self.error_handler,
        )

    @router.setter
    def router(self, new_router: "ABCRouter"):
        self._router = new_router

    @property
    def on(self) -> "ABCLabeler":
        return self.labeler

    @classmethod
    def direct_auth_sync(
        cls: Type["User"],  # type: ignore
        login: str,
        password: str,
        client_id: Optional[int] = None,
        client_secret: Optional[str] = None,
        **kwargs: Any,
    ):
        try:
            loop = asyncio.get_running_loop()
            logger.warning("Event loop is already running, use direct_auth instead")
        except RuntimeError:
            loop = asyncio.new_event_loop()
        return loop.run_until_complete(
            cls.direct_auth(
                login=login,
                password=password,
                client_id=client_id,
                client_secret=client_secret,
                **kwargs,
            )
        )

    @classmethod
    async def direct_auth(
        cls: Type["User"],  # type: ignore
        login: str,
        password: str,
        client_id: Optional[int] = None,
        client_secret: Optional[str] = None,
        **kwargs: Any,
    ):
        token = await UserAuth(client_id, client_secret).get_token(login, password)
        return cls(token=token, **kwargs)


__all__ = ("User",)
