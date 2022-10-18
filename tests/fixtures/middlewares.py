import pytest

from vkbottle.dispatch.middlewares.abc import BaseMiddleware


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
    return {}


@pytest.fixture
def empty_middleware_instance(empty_middleware_class, empty_event):
    return empty_middleware_class(empty_event)
