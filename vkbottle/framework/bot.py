from ..api import Api
from ..handler import Handler, ErrorHandler
from ..const import DEFAULT_BOT_FOLDER
from ..utils import Logger
from ..http import HTTP
from ..api import VKError, HandlerReturnError
from asyncio import get_event_loop, AbstractEventLoop, ensure_future, TimeoutError
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError
from ._event import EventTypes
from .processor import EventProcessor
from .patcher import Patcher
from .branch import BranchManager
from .branch.standart_branch import Branch, ExitBranch


DEFAULT_WAIT = 20


class Bot(HTTP, EventProcessor):
    def __init__(self,
                 token: str,
                 group_id: int,
                 debug: bool = True,
                 plugin_folder: str = None,
                 log_to_file: bool = True,
                 log_to: str = None):
        self.__token: str = token
        self.__group_id: int = group_id
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug = debug
        self.__wait = None
        self.__dispatched = False

        self.api = Api(loop=self.__loop, token=token, group_id=group_id)
        self.patcher = Patcher(plugin_folder or DEFAULT_BOT_FOLDER)

        self._logger = Logger(debug,
                              log_file=log_to,
                              plugin_folder=self.patcher.plugin_folder,
                              logger_enabled=log_to_file)

        self.branch = BranchManager(plugin_folder or DEFAULT_BOT_FOLDER)
        self.on = Handler(self._logger, group_id)
        self.error_handler = ErrorHandler()

    @property
    def group_id(self):
        return self.__group_id

    @property
    def get_loop(self):
        return self.__loop

    @property
    def same(self):
        return self

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
                longPollServer['server'],
                longPollServer['key'],
                longPollServer['ts'],
                self.__wait or DEFAULT_WAIT
            )
            return await self.request.post(url)
        except TimeoutError:
            self._logger.error('TimeoutError of asyncio in longpoll request')
            return await self.make_long_request(longPollServer)

    def run_polling(self):
        loop = self.__loop
        try:
            loop.run_until_complete(self._run_polling())
        except KeyboardInterrupt:
            self._logger.warning('KB interrupt')

    async def _run_polling(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        self._logger.info('LongPoll will be runned. Is it OK?')

        longPollServer = await self.get_server()

        while True:
            try:
                event = await self.make_long_request(longPollServer)
                ensure_future(self.emulate(event))
                longPollServer = await self.get_server()

            except ClientConnectionError or ServerTimeoutError or TimeoutError:
                # No internet connection
                await self._logger.warning('Server Timeout Error!')

    async def emulate(self, event: dict, confirmation_token: str = None):
        if not self.__dispatched:
            self.on.dispatch()
            self.__dispatched = True

        if 'type' in event and event['type'] == 'confirmation':
            if event['group_id'] == self.group_id:
                return confirmation_token or 'dissatisfied'

        updates = event['updates'] if 'updates' in event else [event]
        try:

            for update in updates:
                obj = update['object']

                if update['type'] == EventTypes.MESSAGE_NEW:
                    if obj['peer_id'] < 2e9:
                        if obj['from_id'] not in self.branch.queue:
                            task = ensure_future(self._private_message_processor(obj=obj))
                        else:
                            task = ensure_future(self._branched_processor(obj=obj))
                    else:
                        if 'action' not in obj:
                            if obj['peer_id'] not in self.branch.queue:
                                task = ensure_future(self._chat_message_processor(obj=obj))
                            else:
                                task = ensure_future(self._branched_processor(obj=obj))
                        else:
                            task = ensure_future(self._chat_action_processor(obj=obj))

                    processed = await task
                    ensure_future(self._handler_return(processed, obj))

                else:
                    # If this is an event of the group AND this is not SELF-EVENT
                    task = ensure_future(self._event_processor(obj=obj, event_type=update['type']))
                    await task

        except VKError as e:
            e = list(e.args)[0]
            if e[0] in self.error_handler.get_processor():
                handler = self.error_handler.get_processor()[e[0]]['call']
                self._logger.debug('VKError ?{}! Processing it with handler <{}>'.format(e, handler.__name__))
                ensure_future(handler(e))
            else:
                self._logger.error('VKError! Add @bot.error_handler({}) to process this error!'.format(e))
                raise VKError(e)

        return 'ok'

    def process(self, event: dict, confirmation_token: str = None) -> str:
        status = self.__loop.run_until_complete(self.emulate(event, confirmation_token))
        return status
