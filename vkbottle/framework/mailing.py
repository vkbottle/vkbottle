from ..http import HTTP
from .bot import Bot
from ..api.exceptions import MailingAPIError
from ..utils import Logger
import json


MAILING_LOG_PARAMS = {
    "debug": True,
    "log_file": "mailing.log",
    "plugin_folder": "mailing",
}
API_URL = "https://broadcast.vkforms.ru/api/v2/broadcast?token={}"


class Mailing:
    def __init__(self, token: str, bot: Bot = None):
        self.api_url = API_URL.format(token)
        self._data = None
        self._logger = Logger(
            **(bot._logger.logger_params if bot else MAILING_LOG_PARAMS),
            prefix="Mailing",
            prefix_color="red"
        )

    def __call__(self, list_ids: list = None, user_ids: list = None):

        if not list_ids and not user_ids:
            raise MailingAPIError("You should match list_ids or user_ids")

        self._logger.info("Added new mailing for", list_ids or user_ids)
        return ReadyMailing(self._logger, self.api_url, list_ids, user_ids)


class ReadyMailing(HTTP):
    data: dict = dict()

    def __init__(self, logger: Logger, api_url: str, list_ids: list, user_ids: list):
        self.data["list_ids" if list_ids else "user_ids"] = list_ids or user_ids
        self._api_url: str = api_url
        self.logger: Logger = logger

    def __call__(self, message: str = None, **kwargs):
        self.data["message"] = dict()
        if message:
            self.data["message"]["message"] = message
        if len(kwargs):
            for k, v in kwargs.items():
                self.data["message"][k] = v
        self.data = {**self.data}

        return self

    async def run_now(self):
        if self.data:
            self.data["run_now"] = 1
            self.logger.debug("Mailing will be runned now!")
            return await self.request.post(self._api_url, json=self.data)
        else:
            raise MailingAPIError("Firstly add other params")

    async def run_at(self, utc: str):
        if self.data:
            self.data["run_at"] = utc
            self.logger.debug("Mailing will be runned at", utc)
            return await self.request.post(self._api_url, json=self.data)
        else:
            raise MailingAPIError("Firstly add other params")
