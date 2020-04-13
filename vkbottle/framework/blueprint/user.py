import typing

from vkbottle.api import exceptions, api
from vkbottle.framework.framework.handler import (
    UserHandler,
    ErrorHandler,
)

from .abc import AbstractBlueprint


class Blueprint(AbstractBlueprint):
    def __init__(self, name: str = None, description: str = None) -> None:
        super().__init__()
        # Main workers
        self.on: UserHandler = UserHandler()
        self.error_handler = ErrorHandler()

        self.api: api.Api = None
        self._name: str = name or "Unknown"
        self._description: str = description or "Unknown"

    def create(self, *, api_instance: api.UserApi):
        self.api = api_instance
