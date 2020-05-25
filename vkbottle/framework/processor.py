from vkbottle.utils.constructor import Constructor
from vkbottle.api import API
from .framework.handler.handler import ABCHandler
from .framework.handler import MiddlewareExecutor
from .status import ABCStatus
from .framework.branch.abc import ABCBranchGenerator
from abc import abstractmethod
import typing


class ABCProcessor(Constructor):
    api: API
    handler: ABCHandler
    middleware: MiddlewareExecutor
    status: ABCStatus
    branch: ABCBranchGenerator

    def construct(
        self,
        api: API,
        on: ABCHandler,
        middleware: MiddlewareExecutor,
        status: ABCStatus,
        branch: ABCBranchGenerator,
    ) -> "ABCProcessor":
        """ Construct abstract processor with base active workers """
        self.api = api
        self.handler = on
        self.middleware = middleware
        self.status = status
        self.branch = branch
        return self

    @abstractmethod
    async def parent_processor(self, *args, **kwargs):
        pass

    @abstractmethod
    async def event_processor(self, *args, **kwargs):
        pass

    @abstractmethod
    async def message_processor(self, *args, **kwargs):
        pass

    @abstractmethod
    async def branch_processor(self, *args, **kwargs):
        pass

    @abstractmethod
    async def handler_return(self, handler_return: typing.Any, data: dict) -> bool:
        pass
