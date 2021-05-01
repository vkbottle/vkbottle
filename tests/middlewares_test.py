import pytest

from vkbottle.dispatch.middlewares.abc import BaseMiddleware, MiddlewareError


def test_middleware_send(empty_middleware_instance: BaseMiddleware):
    with pytest.raises(ValueError):
        empty_middleware_instance.send("not_a_dict")

    assert empty_middleware_instance.send() is None


def test_middleware_stop(empty_middleware_instance: BaseMiddleware):
    with pytest.raises(MiddlewareError):
        empty_middleware_instance.stop("some_middleware_error")

    with pytest.raises(ValueError):
        empty_middleware_instance.stop(ValueError("some_value_error"))


def test_constructor_raises_without_pre_and_post():
    class IncompleteMiddleware(BaseMiddleware):
        pass

    with pytest.raises(TypeError):
        IncompleteMiddleware()


@pytest.mark.asyncio
async def test_raise_in_pre_sets_error(empty_middleware_class, empty_event):
    expected_Exception = Exception("some_exception")

    class SomeMiddleware(empty_middleware_class):
        async def pre(self, *args, **kwargs):
            raise expected_Exception

        async def post(self, *args, **kwargs):
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
