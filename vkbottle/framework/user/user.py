import sys
import traceback
import typing
import asyncio

import aiohttp
import vbml

from vkbottle.framework._status import LoggerLevel
from vkbottle.api import UserApi, request
from vkbottle.exceptions import VKError
from vkbottle.framework.framework.handler.user.handler import Handler
from vkbottle.framework.framework.error_handler import (
    VKErrorHandler,
    DefaultErrorHandler,
)
from vkbottle.framework.framework.branch import AbstractBranchGenerator, DictBranch
from vkbottle.framework.framework.handler.middleware import MiddlewareExecutor
from vkbottle.framework.blueprint.user import Blueprint
from vkbottle.http import HTTP, App
from vkbottle.utils import TaskManager, logger
from vkbottle.utils.json import USAGE
from .processor import AsyncHandleManager

try:
    import uvloop
except ImportError:
    uvloop = None


DEFAULT_WAIT = 20
VERSION = 3
MODE = 2

Token = typing.Union[str, typing.List[str]]
AnyUser = typing.Union["User", Blueprint]


class User(HTTP, AsyncHandleManager):
    long_poll_server: dict
    __wait: int
    version: int = None

    def __init__(
        self,
        tokens: Token = None,
        *,
        login: str = None,
        password: str = None,
        user_id: int = None,
        debug: typing.Union[str, bool] = True,
        loop: asyncio.AbstractEventLoop = None,
        expand_models: bool = True,
        mobile: bool = False,
        log_to_path: typing.Union[str, bool] = None,
        vbml_patcher: vbml.Patcher = None,
        mode: int = 234,
        only_asyncio_loop: bool = False,
        **context,
    ):
        self.__tokens = [tokens] if isinstance(tokens, str) else tokens

        self.context: dict = context

        if uvloop is not None:
            if not only_asyncio_loop:
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        if login and password:
            self.__tokens = [self.get_tokens(login, password)]

        self.__loop = loop or asyncio.get_event_loop()
        self.__debug: bool = debug
        self.api: UserApi = UserApi(self.__tokens)
        self.mode = mode

        self._expand_models: bool = expand_models
        self._patcher: vbml.Patcher = vbml_patcher or vbml.Patcher(pattern="^{}$")

        self.user_id: typing.Optional[int] = user_id or self.get_id_by_token(
            self.__tokens[0]
        )
        self.api.user_id = user_id
        UserApi.set_current(self.api)
        self.on: Handler = Handler()
        self.branch: AbstractBranchGenerator = DictBranch()
        self.middleware: MiddlewareExecutor = MiddlewareExecutor()
        self.error_handler: VKErrorHandler = DefaultErrorHandler()

        self._stop: bool = False

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        self.logger = LoggerLevel(debug)
        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<level>[<blue>VKBottle</blue>] {message}</level>",
            filter=self.logger,
            level=0,
            enqueue=mobile is False,
        )
        if log_to_path:
            logger.add(
                "log_user_{time}.log" if log_to_path is True else log_to_path,
                rotation="20 MB",
            )

        logger.info("Using JSON_MODULE - {}".format(USAGE))
        logger.info(
            "Using asyncio loop - {}".format(
                asyncio.get_event_loop_policy().__class__.__module__
            )
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
            raise VKError(0, "Token is invalid")
        return response["response"][0]["id"]

    @staticmethod
    def get_tokens(login: str, password: str, limit: int = 3) -> typing.List[str]:
        app = App(login, password)
        tokens = asyncio.get_event_loop().run_until_complete(
            app.get_tokens(limit=limit)
        )
        return tokens

    def dispatch(self, user: AnyUser):
        """
        Concatenate handlers to current user object
        :param user:
        :return:
        """
        self.on.concatenate(user.on)

    def set_blueprints(self, *blueprints: Blueprint):
        """
        Add blueprints
        """
        for blueprint in blueprints:
            blueprint.create(api_instance=self.api, error_handler=self.error_handler)
            self.dispatch(blueprint)
        logger.debug("Blueprints have been successfully loaded")

    async def get_server(self) -> dict:
        """
        Get longPoll server for long request creation
        :return: server
        """
        self.long_poll_server = (await self.api.messages.get_long_poll_server()).dict()
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
                self.mode,
                self.__wait or DEFAULT_WAIT,
                self.version or VERSION,
            )
            return await self.request.post(url)
        except TimeoutError:
            return await self.make_long_request(long_poll_server)

    async def run(self, wait: int = DEFAULT_WAIT):
        """ Run user polling forever
        Can be manually stopped with:
        >> user.stop()
        """
        self.__wait = wait
        logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        self.on.dispatch()
        logger.debug("User Polling successfully started")

        while not self._stop:
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
                    "While user lp was running error occurred \n\n{}".format(
                        traceback.format_exc()
                    )
                )

        logger.error("Polling was stopped")

    async def emulate(self, event: dict):
        """ Emulate event """
        logger.debug("Response: {}", event)
        for update in event.get("updates", []):
            update_code, update_fields = update[0], update[1:]
            await self._processor(update, update_code, update_fields)

    def run_polling(
        self,
        *,
        auto_reload: bool = False,
        auto_reload_dir: str = ".",
        on_shutdown: typing.Callable = None,
        on_startup: typing.Callable = None,
    ):
        """ Run loop with bot.run() task with loop.run_forever()
        """
        self._stop = False
        task = TaskManager(
            self.__loop,
            auto_reload=auto_reload,
            on_shutdown=on_shutdown,
            on_startup=on_startup,
            auto_reload_dir=auto_reload_dir,
        )
        task.add_task(self.run())
        task.run()

    def stop(self):
        self._stop = True

    @property
    def loop(self):
        return self.__loop

    def __repr__(self):
        return f"<User {self.user_id}>"
