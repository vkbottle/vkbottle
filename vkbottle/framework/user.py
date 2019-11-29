from ..http import HTTP
from ..api import Api
from asyncio import get_event_loop, AbstractEventLoop
import typing


class User(HTTP):
    def __init__(self, token: str, user_id: int = None, debug: bool = False):
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug: bool = debug
        self.__api: Api = Api(self.__loop, token)
        self.user_id: typing.Optional[int] = user_id

    @property
    def api(self):
        return self.__api
