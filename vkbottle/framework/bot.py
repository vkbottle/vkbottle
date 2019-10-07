from ..api import Api
from ..handler import Handler, ErrorHandler
from ..const import DEFAULT_BOT_FOLDER
from ..utils import Logger
from ..http import HTTP
from ..api import VKError
from asyncio import get_event_loop, AbstractEventLoop, ensure_future
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError
from ._event import EventTypes
from .processor import EventProcessor
from .patcher import Patcher


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
        self.on = Handler(self._logger, group_id)
        self.error_handler = ErrorHandler()

    @property
    def group_id(self):
        return self.__group_id

    @property
    def get_loop(self):
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
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
            longPollServer['server'],
            longPollServer['key'],
            longPollServer['ts'],
            self.__wait or DEFAULT_WAIT
        )
        return await self.request.post(url)

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
                ensure_future(self.process(event))
                longPollServer = await self.get_server()

            except ClientConnectionError or ServerTimeoutError:
                # No internet connection
                await self._logger.warning('Server Timeout Error!')

            except VKError as error:
                error = list(error.args)[0]

                if error[0] in self.error_handler.get_processor():
                    handler = self.error_handler.get_processor()[error[0]]['call']

                    self._logger.debug('VKError #{}! Processing it with handler <{}>'.format(error, handler.__name__))
                    ensure_future(handler(error))
                    longPollServer = await self.get_server()

                else:
                    self._logger.error('VKError! Add @bot.error_handler({}) to process this error!'.format(error))
                    raise VKError(error)

    async def process(self, event: dict, confirmation_token: str = None):
        if not self.__dispatched:
            self.on.dispatch()
            self.__dispatched = True

        if 'type' in event and event['type'] == 'confirmation':
            if event['group_id'] == self.group_id:
                return confirmation_token or 'dissatisfied'

        updates = event['updates'] if 'updates' in event else [event]

        for update in updates:
            obj = update['object']

            if update['type'] == EventTypes.MESSAGE_NEW:
                if obj['peer_id'] < 2e9:
                    ensure_future(self._private_message_processor(obj=obj))
                else:
                    if 'action' not in obj:
                        ensure_future(self._chat_message_processor(obj=obj))
                    else:
                        ensure_future(self._chat_action_processor(obj=obj))

            else:
                if obj['from_id'] != -self.group_id:
                    # If this is an event of the group AND this is not SELF-EVENT
                    ensure_future(self._event_processor(obj=obj, event_type=update['type']))

        return 'ok'
