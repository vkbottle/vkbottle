import traceback
from asyncio import get_event_loop, AbstractEventLoop
from asyncio import TimeoutError as AsyncioTimeoutError
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError

from ..const import DEFAULT_BOT_FOLDER, VBML_INSTALL
from ..api import Api, request
from ..handler import Handler, ErrorHandler
from ..utils.logger import Logger, keyboard_interrupt
from ..http import HTTP
from ..api import VKError
from vbml import Patcher, PatchedValidators
from ._event import EventTypes
from .processor import EventProcessor
from .branch import BranchManager
from ..utils.tools import folder_checkup
from ._status import BotStatus

try:
    import vbml
except ImportError:
    print("Please install vbml to use VKBottle. Use command: {}".format(VBML_INSTALL))


DEFAULT_WAIT = 20


class DefaultValidators(PatchedValidators):
    pass


class Bot(HTTP, EventProcessor):
    long_poll_server: dict

    def __init__(
        self,
        token: str,
        *,
        group_id: int = None,
        debug: bool = True,
        plugin_folder: str = None,
        log_to_file: bool = False,
        log_to: str = None,
        secret: str = None,
    ):
        """
        Init bot
        :param token: bot token
        :param group_id: [auto]
        :param debug: should bot debug messages for emulating
        :param plugin_folder: folder for logs
        :param log_to_file: make logs
        :param log_to: log path
        :param secret: secret vk code for callback
        """
        # Base bot classifiers
        self.__token: str = token
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug: bool = debug
        self.__wait = None
        self.__secret = secret
        self._status: BotStatus = BotStatus()

        # Sign assets
        self.__api: Api = Api(token)
        Api.set_current(self.__api)

        if not Patcher.get_current():
            Patcher.set_current(Patcher(pattern="^{}$", validators=DefaultValidators))

        self._logger: Logger = Logger(
            debug=debug,
            log_file=log_to,
            plugin_folder=folder_checkup(plugin_folder or "vkbottle_bot"),
            logger_enabled=log_to_file,
        )
        self.group_id = group_id or self.get_id_by_token(token)

        # Main workers
        self.branch: BranchManager = BranchManager(plugin_folder or DEFAULT_BOT_FOLDER)
        self.on: Handler = Handler(self._logger, self.group_id)
        self.error_handler: ErrorHandler = ErrorHandler()

    def dispatch(self, ext: "Bot"):
        """
        Concatenate handlers to current bot object
        :param ext:
        :return:
        """
        self.on.concatenate(ext.on)
        self.error_handler.update(ext.error_handler.processors)

    @staticmethod
    def get_id_by_token(token: str):
        """
        Get group id from token
        :param token:
        :return:
        """
        response = get_event_loop().run_until_complete(request(token, "groups.getById"))
        if "error" in response:
            raise VKError("Token is invalid")
        return response["response"][0]["id"]

    def _check_secret(self, event: dict):
        """
        Match secret code with current secret
        :param event:
        :return:
        """
        if self.__secret:
            return event.get("secret") == self.__secret
        return True

    def set_debug(self, debug: bool, **params):
        """
        DEPRECATED
        Set debug regime
        :param debug: debug mode
        :param params: logging params
        :return:
        """
        self.__debug = debug
        self._logger: Logger = Logger(
            debug,
            **params,
            **{
                k: v
                for k, v in self._logger.logger_params.items()
                if k not in {**params, "debug": None}
            },
        )

    def loop_update(self, loop: AbstractEventLoop = None):
        """
        Update event loop
        :param loop:
        :return:
        """
        self.__loop = loop or get_event_loop()
        return self.__loop

    def empty_copy(self) -> "Bot":
        """
        Create an empty copy of Bot
        :return: Bot
        """
        copy = Bot(self.__token, group_id=self.group_id, debug=self.__debug,)
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

    @property
    def status(self) -> BotStatus:
        return self._status

    @property
    def loop(self):
        return self.__loop

    @property
    def api(self):
        return self.__api

    @property
    def patcher(self):
        return Patcher.get_current()

    async def get_server(self) -> dict:
        """
        Get longPoll server for long request create
        :return: LongPoll Server
        """
        self.long_poll_server = await self.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        return self.long_poll_server

    async def make_long_request(self, long_poll_server: dict) -> dict:
        """
        Make longPoll request to the VK Server
        :param long_poll_server:
        :return: VK LongPoll Event
        """
        try:
            url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
                long_poll_server["server"],
                long_poll_server["key"],
                long_poll_server["ts"],
                self.__wait or DEFAULT_WAIT,
            )
            return await self.request.post(url)
        except AsyncioTimeoutError:
            self._logger.error("TimeoutError of asyncio in longpoll request")
            return await self.make_long_request(long_poll_server)

    def run_polling(self):
        """
        :return:
        """
        loop = self.__loop
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            keyboard_interrupt()

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        self._logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        self._logger.debug("Polling successfully started. Press Ctrl+C to stop it")

        while True:
            try:
                event = await self.make_long_request(self.long_poll_server)
                if isinstance(event, dict):
                    self.loop.create_task(self.emulate(event))
                await self.get_server()

            except (ClientConnectionError, ServerTimeoutError, AsyncioTimeoutError):
                # No internet connection
                await self._logger.warning("Server Timeout Error!")

    async def emulate(self, event: dict, confirmation_token: str = None) -> str:
        """
        Process all types of events
        :param event: VK Event (LP or CB)
        :param confirmation_token: code which confirm VK callback
        :return: "ok"
        """

        if not self.status.dispatched:
            await self.on.dispatch(self.get_current_rest)
            self.status.dispatched = True

        if event.get("type") == "confirmation":
            if event.get("group_id") == self.group_id:
                return confirmation_token or "dissatisfied"

        updates = event.get("updates", [event])
        if not self._check_secret(event):
            return "access denied"

        try:
            for update in updates:
                obj = update["object"]

                if update["type"] == EventTypes.MESSAGE_NEW:

                    # VK API v5.103
                    client_info = obj.get("client_info")
                    if not client_info:
                        raise VKError("Change API version to 5.103 or later") from None
                    obj = obj["message"]

                    await self._processor(obj, client_info)

                else:
                    # If this is an event of the group AND this is not SELF-EVENT
                    await (
                        self._event_processor(obj=obj, event_type=update["type"])
                    )  # noqa

        except VKError as e:

            e = list(e.args)[0]
            if e[0] in self.error_handler.processors:
                handler = self.error_handler.processors[e[0]]["call"]
                self._logger.debug(
                    "VKError ?{}! Processing it with handler <{}>".format(
                        e, handler.__name__
                    )
                )
                await handler(e)
            else:
                self._logger.error(
                    "VKError! Add @bot.error_handler({}) to process this error!".format(
                        e
                    )
                )
                raise VKError(e)

        except:
            self._logger.error(
                "While bot worked error occurred TIME %#%\n\n{}".format(
                    traceback.format_exc()
                )
            )

        return "ok"

    def process(self, event: dict, confirmation_token: str = None) -> str:
        """
        WHAT THE SHIT I MADE OH MY GODNESS!!!!
        :param event: VK Event
        :param confirmation_token: code which confirms VK callback
        :return: "ok"
        """
        status = self.__loop.run_until_complete(self.emulate(event, confirmation_token))
        return status

    def __repr__(self) -> str:
        return "<Bot {}>".format(self.status.readable)

    def __str__(self) -> str:
        return self.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.close()

    @property
    def __dict__(self) -> dict:
        return self.status.readable

    @property
    def eee(self):
        return "We love you <3"
