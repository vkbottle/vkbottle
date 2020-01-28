from ..http import HTTP
from ..api import UserApi
from ..handler import UserHandler
from asyncio import get_event_loop, AbstractEventLoop
from ..utils import Logger, keyboard_interrupt
from ..utils.tools import folder_checkup
import typing
import aiohttp


DEFAULT_WAIT = 20
VERSION = 3
MODE = 2


class User(HTTP):
    longPollServer: dict
    __wait: int
    _mode: int = None
    version: int = None

    def __init__(
            self,
            token: str,
            user_id: int = None,
            debug: bool = True,
            plugin_folder: str = None,
            mode: int = None,
            log_to_file: bool = False,
    ):
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug: bool = debug
        self.__api: UserApi = UserApi(token)
        UserApi.set_current(self.__api)
        self._mode = mode

        self.user_id: typing.Optional[int] = user_id
        self.on: UserHandler = UserHandler(self._mode)
        self._logger: Logger = Logger(
            debug,
            plugin_folder=folder_checkup(plugin_folder or "vkbottle_user_lp"),
            logger_enabled=log_to_file,
            prefix="User LP VKBottle"
        )

    @property
    def api(self):
        return self.__api

    async def get_server(self):
        """
        Get longPoll server for long request creation
        :return:
        """
        self.longPollServer = await self.api.messages.getLongPollServer()
        return self.longPollServer

    async def make_long_request(self, longPollServer: dict) -> dict:
        """
        Make longPoll request to the VK Server
        :param longPollServer:
        :return: VK LongPoll Event
        """
        try:
            url = "https://{}?act=a_check&key={}&ts={}&wait={}&mode={}&version={}".format(
                longPollServer["server"],
                longPollServer["key"],
                longPollServer["ts"],
                self.__wait or DEFAULT_WAIT,
                self.mode or MODE,
                self.version or VERSION,
            )
            return await self.request.post(url)
        except TimeoutError:
            return await self.make_long_request(longPollServer)

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        self._logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        self._logger.debug("Polling successfully started")

        while True:
            try:
                event = await self.make_long_request(self.longPollServer)
                if isinstance(event, dict):
                    self.__loop.create_task(self.emulate(event))
                await self.get_server()

            except aiohttp.ClientConnectionError or aiohttp.ServerTimeoutError or TimeoutError:
                # No internet connection
                await self._logger.warning("Server Timeout Error!")

    async def emulate(self, event: dict):
        for update in event.get("updates", []):
            update_fields = update[1:]
            for rule in self.on.rules:
                check = await rule.check(update)
                if check is not None:
                    fields, name = rule.data["data"], rule.data["name"]
                    data = dict(zip(fields, update_fields))
                    args, kwargs = [], {}
                    if rule.data.get("dataclass"):
                        data = rule.data.get("dataclass")(**data)
                    if isinstance(check, tuple):
                        if all([await s_rule.check(data) for s_rule in check]):
                            args = (
                                [a for rule in check for a in rule.context.args]
                            )
                            kwargs = (
                                {k: v for rule in check for k, v in rule.context.kwargs.items()}
                            )
                        else:
                            continue

                    await rule.call(data, *args, **kwargs)

    def run_polling(self):
        loop = self.__loop
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            keyboard_interrupt()

    def mode(self, mode: int):
        self._mode = mode
        self.on.mode = mode

    @property
    def loop(self):
        return self.__loop
