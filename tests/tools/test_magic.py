import functools

from vkbottle.tools.magic import get_default_args, magic_bundle


def test_get_default_args_with_keyword_only():
    def func(a, b=1, *, c=2): ...

    # Positional defaults must map to positional params; keyword-only defaults to
    # keyword-only params. They must not be shuffled onto the wrong names.
    assert get_default_args(func) == {"b": 1, "c": 2}


def test_magic_bundle_handles_callable_object():
    class Handler:
        async def __call__(self, event, foo=1): ...

    # A callable instance has no __code__ of its own; magic_bundle must introspect
    # its __call__ instead of raising AttributeError.
    assert magic_bundle(Handler(), {"foo": 9, "bar": 2}) == {"foo": 9}


def test_magic_bundle_does_not_crash_on_partial():
    async def handler(event, foo=1): ...

    # A functools.partial has no __code__; magic_bundle must degrade gracefully
    # instead of raising AttributeError.
    assert isinstance(magic_bundle(functools.partial(handler), {"foo": 5}), dict)
