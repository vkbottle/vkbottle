import typing, traceback, sys
from asyncio import get_event_loop, AbstractEventLoop
from loguru import logger

import aiohttp, vbml

from ..http import HTTP
from ..api import UserApi
from ..handler import UserHandler
from ._status import LoggerLevel


DEFAULT_WAIT = 20
VERSION = 3
MODE = 2


class User(HTTP):
    long_poll_server: dict
    __wait: int
    _mode: int = None
    version: int = None

    def __init__(
        self,
        token: str,
        user_id: int = None,
        debug: bool = True,
        mode: int = None,
        log_to_path: typing.Union[str, bool] = None,
        vbml_patcher: vbml.Patcher = None,
    ):
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug: bool = debug
        self.__api: UserApi = UserApi(token)
        UserApi.set_current(self.__api)
        self._mode = mode
        self._patcher: vbml.Patcher = vbml_patcher or vbml.Patcher(pattern="^{}$")

        self.user_id: typing.Optional[int] = user_id
        self.on: UserHandler = UserHandler(self._mode)

        self.logger = LoggerLevel("INFO" if debug else "ERROR")
        logger.remove()
        logger.add(sys.stderr,
                   colorize=True,
                   format="<level>[<blue>User LP</blue>] {message}</level>",
                   filter=self.logger,
                   level=0,
                   enqueue=True)
        if log_to_path:
            logger.add("log_user_{time}.log" if log_to_path is True else log_to_path, rotation="100 MB")

    @property
    def api(self):
        return self.__api

    async def get_server(self):
        """
        Get longPoll server for long request creation
        :return:
        """
        self.long_poll_server = await self.api.messages.getLongPollServer()
        return self.long_poll_server

    async def make_long_request(self, long_poll_server: dict) -> dict:
        """
        Make longPoll request to the VK Server
        :param long_poll_server:
        :return: VK LongPoll Event
        """
        try:
            url = "https://{}?act=a_check&key={}&ts={}&wait={}&mode={}&version={}".format(
                long_poll_server["server"],
                long_poll_server["key"],
                long_poll_server["ts"],
                self.__wait or DEFAULT_WAIT,
                self.mode or MODE,
                self.version or VERSION,
            )
            return await self.request.post(url)
        except TimeoutError:
            return await self.make_long_request(long_poll_server)

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        logger.debug("Polling successfully started")

        while True:
            try:
                event = await self.make_long_request(self.long_poll_server)
                if isinstance(event, dict):
                    self.__loop.create_task(self.emulate(event))
                await self.get_server()

            except (
                aiohttp.ClientConnectionError,
                aiohttp.ServerTimeoutError,
                TimeoutError,
            ):
                # No internet connection
                await self._logger.warning("Server Timeout Error!")

            except:
                self._logger.error(
                    "While user lp worked error occurred TIME %#%\n\n{}".format(
                        traceback.format_exc()
                    )
                )

    async def emulate(self, event: dict):
        for update in event.get("updates", []):
            update_fields = update[1:]
            for rule in self.on.rules:
                check = await rule.check(update)
                if check is not None:
                    fields, _ = rule.data["data"], rule.data["name"]
                    data = dict(zip(fields, update_fields))
                    args, kwargs = [], {}
                    if rule.data.get("dataclass"):
                        data = rule.data.get("dataclass")(**data)
                    if isinstance(check, tuple):
                        if all([await s_rule.check(data) for s_rule in check]):
                            args = [a for rule in check for a in rule.context.args]
                            kwargs = {
                                k: v
                                for rule in check
                                for k, v in rule.context.kwargs.items()
                            }
                        else:
                            continue

                    await rule.call(data, *args, **kwargs)

    def run_polling(self):
        loop = self.__loop
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            logger.error("Keyboard Interrupt")
            exit(0)

    def mode(self, mode: int):
        self._mode = mode
        self.on.mode = mode

    @property
    def loop(self):
        return self.__loop
