import traceback, sys, typing
from loguru import logger
from asyncio import get_event_loop, AbstractEventLoop
from ..const import DEFAULT_BOT_FOLDER, VBML_INSTALL
from ..api import Api, request
from ..handler import Handler, ErrorHandler
from ..http import HTTP
from ..api import VKError
from ..utils import flatten
from vbml import Patcher, PatchedValidators
from ._event import EventTypes
from .processor import EventProcessor
from .branch import BranchManager
from ._status import BotStatus, LoggerLevel

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
        debug: typing.Union[str, bool] = True,
        log_to_path: typing.Union[str, bool] = None,
        mobile: bool = False,
        secret: str = None,
    ):
        """
        Init bot
        :param token: bot token
        :param group_id: [auto]
        :param debug: should bot debug messages for emulating
        :param log_to_path: make logs
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

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        self.logger = LoggerLevel(debug)

        if not Patcher.get_current():
            Patcher.set_current(Patcher(pattern="^{}$", validators=DefaultValidators))

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
                "log_{time}.log" if log_to_path is True else log_to_path,
                rotation="100 MB",
            )
        self.group_id = group_id or self.get_id_by_token(token)

        # Main workers
        self.branch: BranchManager = BranchManager(DEFAULT_BOT_FOLDER)
        self.on: Handler = Handler(self.group_id)
        self.error_handler: ErrorHandler = ErrorHandler()

    def dispatch(self, ext: "Bot"):
        """
        Concatenate handlers to current bot object
        :param ext:
        :return:
        """
        self.on.concatenate(ext.on)
        self.error_handler.update(ext.error_handler.processors)
        logger.debug("Bot has been successfully dispatched")

    @staticmethod
    def get_id_by_token(token: str):
        """
        Get group id from token
        :param token:
        :return:
        """
        logger.debug("Making API request groups.getById to get group_id")
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
            logger.debug(
                "Checking secret for event ({secret})", secret=event.get("secret")
            )
            return event.get("secret") == self.__secret
        return True

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
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
            long_poll_server["server"],
            long_poll_server["key"],
            long_poll_server["ts"],
            self.__wait,
        )
        return await self.request.post(url)

    def run_polling(self):
        """
        :return:
        """
        loop = self.__loop
        try:
            loop.create_task(self.run())
            loop.run_forever()
        except KeyboardInterrupt:
            logger.error("Keyboard Interrupt")
            exit(0)

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        logger.debug("Polling will be started. Is it OK?")

        if not self.status.dispatched:
            await self.on.dispatch(self.get_current_rest)
            self.status.dispatched = True

        await self.get_server()
        logger.info("Polling successfully started. Press Ctrl+C to stop it")

        while True:
            event = await self.make_long_request(self.long_poll_server)
            await self.get_server()
            self.loop.create_task(self.emulate(event))

    async def emulate(
        self, event: dict, confirmation_token: str = None
    ) -> typing.Union[str, None]:
        """
        Process all types of events
        :param event: VK Event (LP or CB)
        :param confirmation_token: code which confirm VK callback
        :return: "ok"
        """
        if not self.status.dispatched:
            await self.on.dispatch(self.get_current_rest)
            self.status.dispatched = True

        logger.debug("Event: {event}", event=event)

        if event is None:
            return

        if event.get("type") == "confirmation":
            if event.get("group_id") == self.group_id:
                return confirmation_token or "dissatisfied"

        updates = event.get("updates", [event])
        if not self._check_secret(event):
            logger.debug("Aborted. Secret is invalid")
            return "access denied"

        for update in updates:
            if not update:
                continue
            try:
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
                logger.debug(
                    "Error {error}, invented by update: {update}",
                    error=e,
                    update=update,
                )
                if e[0] in self.error_handler.processors:
                    handler = self.error_handler.processors[e[0]]["call"]
                    logger.debug(
                        "VKError ?{}! Processing it with handler <{}>".format(
                            e, handler.__name__
                        )
                    )
                    await handler(e)
                else:
                    logger.error(
                        "VKError! Add @bot.error_handler({}) to process this error!".format(
                            e
                        )
                    )
                    raise VKError(e)

            except:
                logger.error(
                    "While bot worked error occurred \n\n{traceback}",
                    traceback=traceback.format_exc(),
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
