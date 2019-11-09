from ..api import Api
from ..handler import Handler, ErrorHandler
from ..const import DEFAULT_BOT_FOLDER
from ..utils import Logger
from ..http import HTTP
from ..api import VKError
from asyncio import get_event_loop, AbstractEventLoop, TimeoutError
from vbml import Patcher
from vbml.validators import ValidatorManager
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError
from ._event import EventTypes
from .processor import EventProcessor
from .branch import BranchManager
from ..utils import folder_checkup


DEFAULT_WAIT = 20


class Bot(HTTP, EventProcessor):
    def __init__(
        self,
        token: str,
        group_id: int,
        debug: bool = True,
        validators: bool = True,
        plugin_folder: str = None,
        log_to_file: bool = True,
        log_to: str = None,
    ):
        self.__token: str = token
        self.__group_id: int = group_id
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug = debug
        self.__wait = None
        self.__dispatched = False

        self.api = Api(loop=self.__loop, token=token, group_id=group_id)
        self.patcher = Patcher()

        self._logger = Logger(
            debug,
            log_file=log_to,
            plugin_folder=folder_checkup(plugin_folder or 'vkbottle_bot'),
            logger_enabled=log_to_file,
        )

        self.branch = BranchManager(plugin_folder or DEFAULT_BOT_FOLDER)
        self.on = Handler(self._logger, group_id)
        self.error_handler = ErrorHandler()

    @property
    def group_id(self):
        return self.__group_id

    @property
    def loop(self):
        return self.__loop

    async def get_server(self) -> dict:
        """
        Get an longPoll server for long request create
        :return: LongPoll Server
        """
        return await self.api.groups.getLongPollServer(group_id=self.group_id)

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
            loop.run_until_complete(self._run_polling())
        except KeyboardInterrupt:
            self._logger.warning("Keyboard interrupt")

    async def _run_polling(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        self._logger.info("Polling will be started. Is it OK?")

        longPollServer = await self.get_server()
        self._logger.debug('Polling successfully started')

        while True:
            try:
                event = await self.make_long_request(longPollServer)
                if isinstance(event, dict):
                    await self.emulate(event)
                longPollServer = await self.get_server()

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

        if not self.__dispatched:
            await self.on.dispatch(self.get_current_rest)
            self.__dispatched = True

        if event.get("type"):
            if event["group_id"] == self.group_id:
                return confirmation_token or "dissatisfied"

        updates = event.get("updates", [event])

        try:

            for update in updates:
                obj = update["object"]

                if update["type"] == EventTypes.MESSAGE_NEW:

                    # VK API v5.103
                    client_info = obj['client_info']
                    obj = obj['message']

                    if obj["peer_id"] < 2e9:
                        if obj["from_id"] not in self.branch.queue:
                            task = await (
                                self._private_message_processor(obj=obj, client_info=client_info)
                            )
                        else:
                            task = await (
                                self._branched_processor(obj=obj, client_info=client_info)
                            )
                    else:
                        if "action" not in obj:
                            if obj["peer_id"] not in self.branch.queue:
                                task = await (
                                    self._chat_message_processor(obj=obj, client_info=client_info)
                                )
                            else:
                                task = await (
                                    self._branched_processor(obj=obj, client_info=client_info)
                                )
                        else:
                            task = await (
                                self._chat_action_processor(obj=obj, client_info=client_info)
                            )

                    await self._handler_return(task, obj, client_info=client_info)

                else:
                    # If this is an event of the group AND this is not SELF-EVENT
                    task = await (
                        self._event_processor(obj=obj, event_type=update["type"])
                    )

        except VKError as e:
            e = list(e.args)[0]
            if e[0] in self.error_handler.get_processor():
                handler = self.error_handler.get_processor()[e[0]]["call"]
                self._logger.debug(
                    "VKError ?{}! Processing it with handler <{}>".format(e, handler.__name__)
                )
                await handler(e)
            else:
                self._logger.error(
                    "VKError! Add @bot.error_handler({}) to process this error!".format(e)
                )
                raise VKError(e)

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
