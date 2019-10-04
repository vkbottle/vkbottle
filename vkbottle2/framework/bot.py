from ..api import Api
from ..handler import Handler
from ..const import DEFAULT_BOT_FOLDER
from ..utils import Logger
from asyncio import get_event_loop, AbstractEventLoop, ensure_future
from ._event import EventTypes
from .processor import EventProcessor
from .patcher import Patcher


class Bot(EventProcessor):
    def __init__(self,
                 token: str,
                 group_id: int,
                 debug: bool = True,
                 plugin_folder: str = None,
                 log_to: str = None):
        self.__token: str = token
        self.__group_id: int = group_id
        self.__loop: AbstractEventLoop = get_event_loop()
        self.__debug = debug

        self.api = Api(loop=self.__loop, token=token, group_id=group_id)
        self.patcher = Patcher(plugin_folder or DEFAULT_BOT_FOLDER)
        self._logger = Logger(debug, log_file=log_to, plugin_folder=self.patcher.plugin_folder)
        self.on = Handler(self._logger, group_id)

    @property
    def group_id(self):
        return self.__group_id

    @property
    def get_loop(self):
        return self.__loop

    async def process(self, event: dict, confirmation_token: str = None):
        if 'type' in event and event['type'] == 'confirmation':
            if event['group_id'] == self.group_id:
                return confirmation_token or 'dissatisfied'

        for update in event['updates']:
            obj = update['object']

            if update['type'] == EventTypes.MESSAGE_NEW:
                if obj['peer_id'] < 2e9:

                    ensure_future(self._private_message_processor(obj=obj))

                """else:
                    if 'action' not in obj:
                        await self.new_chat_message(obj=obj)
                    else:
                        await self.new_chat_action(obj=obj)"""

            else:
                pass
                # If this is an event of the group
                # await self.new_event(event_type=update['type'], obj=obj)

        return 'ok'


