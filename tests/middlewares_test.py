import pytest

from vkbottle.dispatch.middlewares.abc import BaseMiddleware, MiddlewareError


def test_middleware_send(empty_middleware_instance):
    with pytest.raises(ValueError):
        empty_middleware_instance.send("not_a_dict")

    assert empty_middleware_instance.send() == None


def test_middleware_stop(empty_middleware_instance):
    with pytest.raises(MiddlewareError):
        empty_middleware_instance.stop("some_middleware_error")

    with pytest.raises(ValueError):
        empty_middleware_instance.stop(ValueError("some_value_error"))


def test_constructor_raises_without_pre_and_post():
    class IncompleteMiddleware(BaseMiddleware):
        pass

    with pytest.raises(TypeError):
        IncompleteMiddleware()
