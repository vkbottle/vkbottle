from typing import Any, List, Type

import pytest

from vkbottle.dispatch.middlewares.abc import BaseMiddleware, MiddlewareError
from vkbottle.dispatch.views.abc_dispense import ABCDispenseView
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin


class EmptyMiddleware(BaseMiddleware):
    async def pre(self, *args, **kwargs):
        pass

    async def post(self, *args, **kwargs):
        pass


@pytest.fixture
def empty_middleware_class():
    return EmptyMiddleware


@pytest.fixture
def empty_event():
    return MessageMin()


@pytest.fixture
def empty_middleware_instance(empty_middleware_class, empty_event):
    return empty_middleware_class(empty_event)
