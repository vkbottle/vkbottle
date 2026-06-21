from vkbottle.tools.magic import get_default_args


def test_get_default_args_with_keyword_only():
    def func(a, b=1, *, c=2): ...

    # Positional defaults must map to positional params; keyword-only defaults to
    # keyword-only params. They must not be shuffled onto the wrong names.
    assert get_default_args(func) == {"b": 1, "c": 2}
