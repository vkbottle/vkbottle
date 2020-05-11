import asyncio
import sys
import traceback
import typing
from vbml import Patcher

from vkbottle.http import HTTP
from vkbottle.types.events import EventList
from vkbottle.framework.framework.handler.handler import Handler
from vkbottle.framework.framework.error_handler import (
    VKErrorHandler,
    DefaultErrorHandler,
)
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.framework.framework.extensions import AbstractExtension
from vkbottle.framework.framework.extensions.standard import StandardExtension
from vkbottle.framework._status import BotStatus, LoggerLevel
from vkbottle.framework.framework.branch import DictBranch
from vkbottle.framework.framework.branch.abc import AbstractBranchGenerator
from vkbottle.framework.blueprint.bot import Blueprint
from vkbottle.framework.bot.processor import AsyncHandleManager
from vkbottle.framework.bot.builtin import DefaultValidators, DEFAULT_WAIT
from vkbottle.api import Api, request
from vkbottle.exceptions import VKError
from vkbottle.utils import logger, TaskManager, chunks
from vkbottle.utils.json import USAGE


try:
    import uvloop
except ImportError:
    uvloop = None


Token = typing.Union[str, typing.List[str]]
AnyBot = typing.Union["Bot", Blueprint]


class Bot(HTTP, AsyncHandleManager):
    long_poll_server: dict

    def __init__(
        self,
        tokens: Token = None,
        *,
        group_id: int = None,
        debug: typing.Union[str, bool] = True,
        loop: asyncio.AbstractEventLoop = None,
        throw_errors: bool = True,
        log_to_path: typing.Union[str, bool] = None,
        patcher: Patcher = None,
        mobile: bool = False,
        secret: str = None,
        extension: AbstractExtension = None,
        logs_folder: typing.Optional[str] = None,
        only_asyncio_loop: bool = False,
        **context,
    ):
        """
        Init bot
        :param tokens: bot tokens
        :param group_id:
        :param debug: should bot debug messages for emulating
        :param log_to_path: make logs
        :param secret: secret vk code for callback
        :param extension:
        """
        # Base bot classifiers
        self.__tokens: typing.List[str] = [tokens] if isinstance(
            tokens, str
        ) else tokens
        self.__debug: bool = debug
        self.__wait = None
        self.__secret = secret
        self._status: BotStatus = BotStatus()

        self.context: dict = context

        if uvloop is not None:
            if not only_asyncio_loop:
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        self.logger = LoggerLevel(debug)

        if not Patcher.get_current():
            Patcher.set_current(
                patcher
                if patcher is not None
                else Patcher(pattern="^{}$", validators=DefaultValidators)
            )

        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<level>[<blue>VKBottle</blue>] {message}</level> <white>[TIME {time:HH:MM:ss}]</white>",
            filter=self.logger,
            level=0,
            enqueue=mobile is False,
        )
        logger.level("INFO", color="<white>")
        logger.level("ERROR", color="<red>")
        if log_to_path:
            logger.add(
                (logs_folder or "") + "log_{time}.log"
                if log_to_path is True
                else log_to_path,
                rotation="20 MB",
            )

        self.group_id = group_id or self.get_id_by_token(self.__tokens[0])
        self.__loop = loop or asyncio.get_event_loop()

        # Sign assets
        self.api: Api = Api(self.__tokens, throw_errors=throw_errors)
        self.extension: AbstractExtension = extension if extension is not None else StandardExtension()

        self._throw_errors: bool = throw_errors
        Api.set_current(self.api)
        AbstractExtension.set_current(self.extension)

        # Main workers
        self.branch: typing.Union[AbstractBranchGenerator, DictBranch] = DictBranch()
        self.middleware: MiddlewareExecutor = MiddlewareExecutor()
        self.on: Handler = Handler(self.group_id)
        self.error_handler: VKErrorHandler = DefaultErrorHandler()

        self._stop: bool = False

        logger.info("Using JSON_MODULE - {}".format(USAGE))
        logger.info(
            "Using asyncio loop - {}".format(
                asyncio.get_event_loop_policy().__class__.__module__
            )
        )

    async def get_updates(self):
        # noqa
        logger.info("Receiving updates from conversations")
        updates = []
        close, offset = False, 0

        while not close:
            conversations = await self.api.messages.get_conversations(
                offset, 200, filter="unanswered"
            )
            if offset == 0:
                logger.info(f"Conversation count - {conversations.count}")
                if conversations.count == 0:
                    return
            offset += 200

            updates.extend([item.conversation.out_read for item in conversations.items])
            if len(conversations.items) < 200:
                close = True

        logger.warning("Answering...")

        chunk = list(chunks(updates, 100))
        for mid in chunk:
            try:
                messages = await self.api.messages.get_by_id(mid)
                await self.emulate(
                    {
                        "updates": [
                            {
                                "type": "message_new",
                                "object": {"message": m.dict(), "client_info": {}},
                            }
                            for m in messages.items
                        ]
                    }
                )
            except VKError:
                continue

    async def dispatch(self, bot: AnyBot):
        """
        Concatenate handlers to current bot object
        :param bot:
        :return:
        """
        self.on.concatenate(bot.on)
        self.error_handler.handled_errors.update(bot.error_handler.handled_errors)
        self.middleware.middleware += bot.middleware.middleware
        for branch_name, disposal in (await bot.branch.branches).items():
            self.branch.add_branch(disposal[0], name=branch_name)
        logger.debug("Bot has been successfully dispatched")

    def set_blueprints(self, *blueprints: Blueprint):
        """
        Add blueprints
        """
        for blueprint in blueprints:
            blueprint.create(familiar=(self.branch, self.extension, self.api))
            self.loop.create_task(self.dispatch(blueprint))
        logger.debug("Blueprints have been successfully loaded")

    @staticmethod
    def get_id_by_token(token: str, throw_exc: bool = True) -> typing.Union[int, bool]:
        """
        Get group id from token
        :param token:
        :param throw_exc:
        :return:
        """
        logger.debug("Making API request groups.getById to get group_id")
        response = asyncio.get_event_loop().run_until_complete(
            request("groups.getById", {}, token, throw_errors=False)
        )
        if "error" in response:
            if throw_exc:
                raise VKError(0, "Token is invalid")
            return False
        return response["response"][0]["id"]

    def _check_secret(self, event: dict, secret: typing.Optional[str] = None):
        """
        Match secret code with current secret
        :param event:
        :return:
        """
        if self.__secret or secret:
            logger.debug(
                "Checking secret for event ({secret})", secret=event.get("secret")
            )
            return event.get("secret") == (self.__secret or secret)
        return True

    def executor_api(self, api):
        self.api = api
        Api.set_current(api)

    def loop_update(self, loop: asyncio.AbstractEventLoop = None):
        """
        Update event loop
        :param loop:
        :return:
        """
        self.__loop = loop or asyncio.get_event_loop()
        return self.__loop

    def empty_copy(self) -> "Bot":
        """
        Create an empty copy of Bot
        :return: Bot
        """
        copy = Bot(self.__tokens, group_id=self.group_id, debug=self.__debug,)
        return copy

    def copy(self) -> "Bot":
        """
        Create copy of Bot
        :return: Bot
        """
        bot = self.empty_copy()
        bot.loop_update()
        bot.on = self.on
        bot.branch = self.branch
        bot.error_handler = self.error_handler
        return bot

    async def get_server(self) -> dict:
        """
        Get longPoll server for long request create
        :return: LongPoll Server
        """
        self.long_poll_server = (
            await self.api.groups.get_long_poll_server(group_id=self.group_id)
        ).dict()
        return self.long_poll_server

    async def make_long_request(self, long_poll_server: dict) -> dict:
        """
        Make longPoll request to the VK Server
        :param long_poll_server:
        :return: VK LongPoll Event
        """
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
            long_poll_server["server"],
            long_poll_server["key"],
            long_poll_server["ts"],
            self.__wait,
        )
        return await self.request.post(url)

    def run_polling(
        self,
        *,
        skip_updates: bool = True,
        auto_reload: bool = False,
        auto_reload_dir: str = ".",
        on_shutdown: typing.Callable = None,
        on_startup: typing.Callable = None,
    ):
        """
        :return:
        """
        self._stop = False
        task = TaskManager(
            self.__loop,
            auto_reload=auto_reload,
            on_shutdown=on_shutdown,
            on_startup=on_startup,
            auto_reload_dir=auto_reload_dir,
        )
        task.add_task(self.run(skip_updates))
        task.run()

    async def run(self, skip_updates: bool, wait: int = DEFAULT_WAIT):
        """ Run bot polling forever
        Can be manually stopped with:
        bot.stop()
        """
        self.__wait = wait
        logger.debug("Polling will be started. Is it OK?")
        if self.__secret is not None:
            logger.warning("You set up secret and started polling. Removing secret")
            self.__secret = None

        if not self.status.dispatched:
            self.middleware.add_middleware(self.on.pre)
            await self.on.dispatch(self.get_current_rest)
            self.status.dispatched = True

        if not skip_updates:
            await self.get_updates()

        await self.get_server()
        logger.info("Polling successfully started. Press Ctrl+C to stop it")

        while not self._stop:
            event = await self.make_long_request(self.long_poll_server)
            if isinstance(event, dict) and event.get("ts"):
                self.loop.create_task(self.emulate(event))
                self.long_poll_server["ts"] = event["ts"]
            else:
                await self.get_server()

        logger.error("Polling was stopped")

    async def emulate(
        self, event: dict, confirmation_token: str = None, secret: str = None,
    ) -> typing.Union[str, None]:
        """
        Process all types of events
        :param event: VK Event (LP or CB)
        :param confirmation_token: code which confirm VK callback
        :param secret: secret key for callback
        :return: "ok"
        """
        if not self.status.dispatched:
            self.middleware.add_middleware(self.on.pre)
            await self.on.dispatch(self.get_current_rest)
            self.status.dispatched = True

        logger.debug("Event: {event}", event=event)

        if event is None:
            return

        if event.get("type") == "confirmation":
            if event.get("group_id") == self.group_id:
                return confirmation_token or "dissatisfied"

        updates = event.get("updates", [event])
        if not self._check_secret(event, secret=secret):
            logger.debug("Aborted. Secret is invalid")
            return "access denied"

        for update in updates:
            try:
                if not update.get("object"):
                    continue

                obj = update["object"]

                if update["type"] == EventList.MESSAGE_NEW:

                    # VK API v5.103
                    client_info = obj.get("client_info")
                    if client_info is None:
                        raise VKError(
                            0, "Change API version to 5.103 or later"
                        ) from None
                    obj = obj["message"]
                    await self._processor(obj, client_info)

                else:
                    await (
                        self._event_processor(obj=obj, event_type=update["type"])
                    )  # noqa

            except VKError as e:
                await self.error_handler.handle_error(e)

            except:
                logger.error(
                    "While event was emulating error occurred \n\n{traceback}",
                    traceback=traceback.format_exc(),
                )

        return "ok"

    def stop(self):
        self._stop = True

    def __repr__(self) -> str:
        return "<Bot {}>".format(self.status.as_dict)

    @property
    def __dict__(self) -> dict:
        return self.status.as_dict

    @property
    def status(self) -> BotStatus:
        return self._status

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, loop: asyncio.AbstractEventLoop):
        self.__loop = loop

    @property
    def patcher(self):
        return Patcher.get_current()

    @property
    def eee(self):
        return "We love you <3"
