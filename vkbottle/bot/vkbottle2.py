"""Read LICENSE.txt"""

"""
MAIN BOT LONGPOLL CONSTRUCTOR
"""

from ..portable import __version__ as VERSION, API_VERSION
from ..utils import Logger, HTTP, path_loader, ErrorHandler
from ..vk import exceptions
from ..methods import Method, Api
from .. import notifications as nf
from .events import Events, processor
from aiohttp import ClientSession, ClientConnectionError, ClientTimeout
import asyncio
from .patcher import Patcher
from ..project_collections.color import colored

import time


class LongPollBot(HTTP, processor.UpdatesProcessor):
    """
    Standart LongPoll VK Bot engine

    Use LongPollBot object to manage plugins or use it in its own. Be sure
    """
    wait: int

    def __init__(self, token: str, group_id: int, plugin_folder: str = None,
                 debug: bool = False):
        """
        Bot Main Auth
        :param token: VK Api Token
        :param group_id:
        :param plugin_folder: Path to plugin folder. None if plugins are not in use
        :param debug: Should VKBottle show debugging messages
        """

        self.group_id: int = group_id
        self.logger: Logger = Logger(debug=debug)

        self.session = ClientSession
        self._loop = asyncio.get_event_loop
        self.plugin_folder = path_loader.checkup_plugins(folder=plugin_folder)

        self.on: Events = Events(group_id=self.group_id)
        self._method: Method = Method(token)
        self.api: Api = Api(self._method, group_id=self.group_id)

        self.patcher = Patcher(logger=self.logger, plugin_folder=self.plugin_folder)
        self.error_handler = ErrorHandler()

    def run(self, wait: int = 15):
        """
        Run Bot Async start coroutine
        :param wait: Long Request max waiting time (25 is recommended, max - 90)
        """
        self.wait = wait
        loop = self._loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self._loop().run_until_complete(self.logger.warn(nf.keyboard_interrupt))

    async def start(self):
        """
        LongPoll Bot runner
        todo RU -  сделать нормальную функцию проверки версии
        """
        # [Support] Plugin Support
        # Added v0.20#master
        # self._plugins = await path_loader.load_plugins(folder=self.plugin_folder, logger=self.logger)

        current_portable = await self.get_current_portable()
        """
        Check newest version of VKBottle and alarm if newer version is available
        """
        if current_portable['version'] != VERSION:
            await self.logger(nf.newer_version.format(current_portable['version']))
        else:
            await self.logger(nf.newest_version)

        # [Feature] If LongPoll is not enabled in the group it automatically stops
        # Added v0.19#master
        longPollEnabled = await self.api.request('groups', 'getLongPollSettings', {'group_id': self.group_id})

        if longPollEnabled['is_enabled']:

            # [Feature] Merge messages dictionaries
            # Added v0.20#master
            self.on.merge_processors()

            longPollServer = await self.get_server()
            print(self.on.processor_message_regex)

            await self.logger(nf.module_longpoll.format(API_VERSION),
                              colored('you use: ' + longPollEnabled['api_version'], 'yellow'))

            await self._run(longPollServer)

        else:

            await self.logger.error(nf.longpoll_not_enabled)

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
                    self.wait
                )
        return await self.request.post(url)

    async def _run(self, longPollServer: dict):
        while True:
            try:
                event = await self.make_long_request(longPollServer)
                print(event)
                self.a = time.time()
                await self.new_update(event)
                longPollServer = await self.get_server()

            except ClientConnectionError or ClientTimeout:
                # No internet connection
                await self.logger.warn(nf.request_connection_timeout)

            except exceptions.VKError as error:
                error = list(error.args)[0]
                if error[0] in self.error_handler.get_processor():
                    await self.error_handler.get_processor()[error[0]]['call'](error)
                    longPollServer = await self.get_server()
                else:
                    raise exceptions.VKError(error)
