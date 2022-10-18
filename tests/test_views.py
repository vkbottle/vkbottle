import pytest

from vkbottle import ABCView
from vkbottle.dispatch.middlewares.abc import BaseMiddleware


class SomeView(ABCView):
    def __init__(self, middlewares):
        super().__init__()
        self.middlewares = middlewares

    async def process_event(self):
        pass

    async def handle_event(self):
        pass


@pytest.mark.asyncio
async def test_pre_post_middleware_returns_exception(empty_event):
    expected_error = Exception()

    def construct_exception_middleware(event, view=None):
        instance = BaseMiddleware(event, view=view)
        instance.error = expected_error
        return instance

    middleware = construct_exception_middleware(empty_event)
    assert middleware.error == expected_error
    assert middleware.can_forward is False

    view = SomeView([construct_exception_middleware])
    mw_instances = await view.pre_middleware(empty_event)
    assert mw_instances is None
