from ..const import DEFAULT_BOT_FOLDER, VBML_INSTALL

try:
    import vbml
except ImportError:
    print("Please install vbml to use VKBottle. Use command: {}".format(VBML_INSTALL))

from ..api import Api
from ..handler import Handler, ErrorHandler
from ..utils.logger import Logger, keyboard_interrupt
from ..http import HTTP
from ..api import VKError
from asyncio import get_event_loop, AbstractEventLoop, TimeoutError
from vbml import Patcher, PatchedValidators
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError
from ._event import EventTypes
from .processor import EventProcessor
from .branch import BranchManager
from ..utils.tools import folder_checkup
import traceback
from ._status import BotStatus


DEFAULT_WAIT = 20


class Vals(PatchedValidators):
    pass


class Bot(HTTP, EventProcessor):
    longPollServer: dict

    def __init__(
        self,
        token: str,
        group_id: int,
        debug: bool = True,
        plugin_folder: str = None,
        log_to_file: bool = False,
        log_to: str = None,
        vbml_patcher: Patcher = None,
        secret: str = None,
    ):
        self.__token: str = token
        self.__group_id: int = group_id
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug: bool = debug
        self.__wait = None
        self.__logger_opt = (plugin_folder, log_to_file, log_to)
        self.__vbml_patcher = vbml_patcher
        self.__secret = secret
        self._status: BotStatus = BotStatus()

        self.__api: Api = Api(loop=self.__loop, token=token, group_id=group_id)
        self._patcher: Patcher = vbml_patcher or Patcher(pattern="^{}$")

        self._logger: Logger = Logger(
            debug,
            log_file=log_to,
            plugin_folder=folder_checkup(plugin_folder or "vkbottle_bot"),
            logger_enabled=log_to_file,
        )

        self.branch: BranchManager = BranchManager(plugin_folder or DEFAULT_BOT_FOLDER)
        self.on: Handler = Handler(self._logger, group_id)
        self.error_handler: ErrorHandler = ErrorHandler()

    def dispatch(self, ext: "Bot"):
        self.on.concatenate(ext.on)
        self.error_handler.update(ext.error_handler.processors)

    @property
    def group_id(self):
        return self.__group_id

    def _check_secret(self, secret: str):
        if self.__secret:
            return secret == self.__secret

    def set_debug(self, debug: bool, **params):
        self.__debug = debug
        self._logger: Logger = Logger(
            debug,
            **params,
            **{
                k: v
                for k, v in self._logger.logger_params.items()
                if k not in {**params, "debug": None}
            }
        )

    def loop_update(self, loop: AbstractEventLoop = None):
        self.__loop = loop or get_event_loop()
        return self.__loop

    def empty_copy(self) -> "Bot":
        copy = Bot(
            self.__token,
            self.__group_id,
            self.__debug,
            *self.__logger_opt,
            self.__vbml_patcher
        )
        return copy

    def copy(self) -> "Bot":
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
        return self._patcher

    async def get_server(self) -> dict:
        """
        Get an longPoll server for long request create
        :return: LongPoll Server
        """
        self.longPollServer = await self.api.groups.getLongPollServer(
            group_id=self.group_id
        )
        return self.longPollServer

    async def make_long_request(self, longPollServer: dict) -> dict:
        """
        Make longPoll request to the VK Server. Comes off after wait time
        :param longPollServer:
        :return: VK LongPoll Event
        """
        try:
            url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
                longPollServer["server"],
                longPollServer["key"],
                longPollServer["ts"],
                self.__wait or DEFAULT_WAIT,
            )
            return await self.request.post(url)
        except TimeoutError:
            self._logger.error("TimeoutError of asyncio in longpoll request")
            return await self.make_long_request(longPollServer)

    def run_polling(self):
        loop = self.__loop
        try:
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            keyboard_interrupt()

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        self._logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        self._logger.debug("Polling successfully started")

        while True:
            try:
                event = await self.make_long_request(self.longPollServer)
                if isinstance(event, dict):
                    self.loop.create_task(self.emulate(event))
                await self.get_server()

            except ClientConnectionError or ServerTimeoutError or TimeoutError:
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
        if "secret" in event:
            if not self._check_secret(event["secret"]):
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
                    processor = dict(obj=obj, client_info=client_info)

                    if obj["peer_id"] < 2e9:
                        if obj["from_id"] not in self.branch.queue:
                            task = await self._private_message_processor(**processor)
                        else:
                            task = await self._branched_processor(**processor)
                    else:
                        if obj["peer_id"] not in self.branch.queue:
                            task = await self._chat_message_processor(**processor)
                        else:
                            task = await self._branched_processor(**processor)

                    await self._handler_return(task, **processor)

                else:
                    # If this is an event of the group AND this is not SELF-EVENT
                    task = await (
                        self._event_processor(obj=obj, event_type=update["type"])
                    )

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

        except Exception as e:
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
