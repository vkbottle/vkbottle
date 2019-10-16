from ..http import HTTP
from .bot import Bot
from ..api.exceptions import MailingAPIError
from ..utils import Logger
import json


MAILING_LOG_PARAMS = {'debug': True, 'log_file': 'mailing.log', 'plugin_folder': 'mailing'}


class Mailing(HTTP):
    def __init__(self,
                 token: str,
                 bot: Bot = None,
                 access_token: str = None,
                 debug: bool = False):
        self.__token = access_token or token
        self.api_url = 'https://broadcast.vkforms.ru/api/v2/broadcast'
        self._data = None
        self._logger = Logger(
            **(bot._logger.logger_params if bot else MAILING_LOG_PARAMS),
            prefix='Mailing', prefix_color='red')

    def __call__(self,
                 message: dict,
                 list_ids: list = None,
                 user_ids: list = None):

        if not list_ids and not user_ids:
            raise MailingAPIError('You should match list_ids or user_ids')

        self._data = dict(message=message)
        self._data['list_ids' if list_ids else 'user_ids'] = list_ids or user_ids
        self._logger.info('Added new mailing for', list_ids or user_ids)

    def message(self, message: dict):
        self._data['message'] = message

    async def run_now(self):
        if self._data:
            self._data['run_now'] = 1
            self._logger.debug('Mailing will be runned now!')
            return await self.request.post(f'{self.api_url}?token={self.__token}', json=self._data)
        else:
            raise MailingAPIError('Firstly add other params')

    async def run_at(self, utc: str):
        if self._data:
            self._data['run_at'] = utc
            self._logger.debug('Mailing will be runned at', utc)
            return await self.request.post(f'{self.api_url}?token={self.__token}', json=self._data)
        else:
            raise MailingAPIError('Firstly add other params')
