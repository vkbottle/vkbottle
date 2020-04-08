import sys
import traceback
import typing
import asyncio

import aiohttp
import vbml

from vkbottle.framework._status import LoggerLevel
from vkbottle.api import UserApi, VKError, request
from vkbottle.framework.framework.handler import UserHandler
from vkbottle.http import HTTP
from vkbottle.utils import logger

DEFAULT_WAIT = 20
VERSION = 3
MODE = 2
Token = typing.Union[str, typing.List[str]]


class User(HTTP):
    long_poll_server: dict
    __wait: int
    _mode: int = None
    version: int = None

    def __init__(
        self,
        tokens: Token = None,
        user_id: int = None,
        debug: bool = True,
        expand_models: bool = True,
        log_to_path: typing.Union[str, bool] = None,
        vbml_patcher: vbml.Patcher = None,
    ):
        self.__tokens = [tokens] if isinstance(tokens, str) else tokens
        self.__loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.__debug: bool = debug
        self.api: UserApi = UserApi(self.__tokens)
        UserApi.set_current(self.api)

        self._expand_models: bool = expand_models
        self._patcher: vbml.Patcher = vbml_patcher or vbml.Patcher(pattern="^{}$")

        self.user_id: typing.Optional[int] = user_id or self.get_id_by_token(
            self.__tokens[0]
        )
        self.on: UserHandler = UserHandler(self._mode)

        self.logger = LoggerLevel("INFO" if debug else "ERROR")
        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<level>[<blue>VKBottle</blue>] {message}</level>",
            filter=self.logger,
            level=0,
            enqueue=True,
        )
        if log_to_path:
            logger.add(
                "log_user_{time}.log" if log_to_path is True else log_to_path,
                rotation="100 MB",
            )

    @staticmethod
    def get_id_by_token(token: str):
        """
        Get group id from token
        :param token:
        :return:
        """
        logger.debug("Making API request users.get to get user_id")
        response = asyncio.get_event_loop().run_until_complete(
            request("users.get", {}, token)
        )
        if "error" in response:
            raise VKError("Token is invalid")
        return response["response"][0]["id"]

    async def get_server(self):
        """
        Get longPoll server for long request creation
        :return:
        """
        self.long_poll_server = (await self.api.messages.get_long_poll_server()).dict()
        return self.long_poll_server

    async def make_long_request(self, long_poll_server) -> dict:
        """
        Make longPoll request to the VK Server
        :param long_poll_server:
        :return: VK LongPoll Event
        """
        try:
            url = "https://{}?act=a_check&key={}&ts={}&wait={}&mode=234&version={}".format(
                long_poll_server["server"],
                long_poll_server["key"],
                long_poll_server["ts"],
                self.__wait or DEFAULT_WAIT,
                self.version or VERSION,
            )
            return await self.request.post(url)
        except TimeoutError:
            return await self.make_long_request(long_poll_server)

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        logger.debug("User Polling successfully started")

        while True:
            try:
                event = await self.make_long_request(self.long_poll_server)
                if isinstance(event, dict) and event.get("ts"):
                    self.__loop.create_task(self.emulate(event))
                    self.long_poll_server["ts"] = event["ts"]
                else:
                    await self.get_server()

            except (
                aiohttp.ClientConnectionError,
                aiohttp.ServerTimeoutError,
                TimeoutError,
            ):
                # No internet connection
                logger.warning("Server Timeout Error!")

            except:
                logger.error(
                    "While user lp worked error occurred \n\n{}".format(
                        traceback.format_exc()
                    )
                )

    async def emulate(self, event: dict):
        for update in event.get("updates", []):
            update_code, update_fields = update[0], update[1:]

            for rule in self.on.rules:
                check = await rule.check(update)

                if check is not None:
                    fields, _ = rule.data["data"], rule.data["name"]
                    data = dict(zip(fields, update_fields))
                    args, kwargs = [], {}

                    if self._expand_models:
                        data.update(await self.expand_data(update_code, data))

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

                    task = await rule.call(data, *args, **kwargs)

                    if task is not None:
                        await data(str(task))

    def run_polling(self):
        loop = self.__loop
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            logger.error("Keyboard Interrupt")
            exit(0)

    async def expand_data(self, code: int, data):
        if code in range(6):
            data.update(
                (
                    await self.api.messages.get_by_id(message_ids=data["message_id"])
                ).items[0].dict()
            )
        return data

    def mode(self, mode: int):
        raise VKError(
            "User LP mode specifier is abandoned, mode 234 is used as default. See issue #36"
        )

    @property
    def loop(self):
        return self.__loop
