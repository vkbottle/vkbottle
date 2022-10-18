import pytest

from vkbottle.dispatch.middlewares.abc import BaseMiddleware, MiddlewareError
from vkbottle.dispatch.views.bot.message import BotMessageView


def test_middleware_send(empty_middleware_instance: BaseMiddleware):
    with pytest.raises(ValueError):
        empty_middleware_instance.send("not_a_dict")  # type: ignore

    assert empty_middleware_instance.send() is None


def test_middleware_stop(empty_middleware_instance: BaseMiddleware):
    with pytest.raises(MiddlewareError):
        empty_middleware_instance.stop()

    with pytest.raises(MiddlewareError):
        empty_middleware_instance.stop("some_middleware_error")

    with pytest.raises(ValueError):
        empty_middleware_instance.stop(ValueError("some_value_error"))


def test_middleware_constructs_without_pre_and_post(empty_event):
    class IncompleteMiddleware(BaseMiddleware):
        pass

    IncompleteMiddleware(empty_event)


@pytest.mark.asyncio
async def test_raise_in_pre_sets_error(empty_middleware_class, empty_event):
    expected_Exception = Exception("some_exception")

    class SomeMiddleware(empty_middleware_class):
        async def pre(self):
            raise expected_Exception

        async def post(self):
            raise expected_Exception

    middleware = SomeMiddleware(empty_event)

    await middleware.pre()
    assert middleware.error == expected_Exception

    await middleware.post()
    assert middleware.error == expected_Exception


@pytest.mark.asyncio
async def test_cant_forward_on_error(empty_middleware_class, empty_event):
    class SomeMiddleware(empty_middleware_class):
        async def pre(self, *args, **kwargs):
            self.error("some_error")

    middleware = SomeMiddleware(empty_event)

    await middleware.pre()
    assert middleware.can_forward is False


@pytest.mark.asyncio
async def test_view_middleware_utils_run(empty_event):
    view = BotMessageView()
    mw_instances = await view.pre_middleware(empty_event, {})
    if mw_instances:
        await view.post_middleware(mw_instances)
