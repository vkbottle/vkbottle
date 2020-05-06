from vkbottle.api import api
from vkbottle.framework.framework.error_handler import (
    VKErrorHandler,
    DefaultErrorHandler,
)
from vkbottle.framework.framework.handler.user.handler import Handler

from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.on: Handler = Handler()
        self.error_handler: VKErrorHandler = DefaultErrorHandler()

        self.api: api.Api = None
        self._name: str = name or "Unknown"
        self._description: str = description or "Unknown"

    def create(self, *, api_instance: api.UserApi, error_handler: VKErrorHandler):
        self.api = api_instance
        self.error_handler = error_handler
