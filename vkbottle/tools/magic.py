import types
import typing

Function = typing.Union[
    typing.Callable[..., typing.Any],
    types.FunctionType,
]


def resolve_arg_names(func: Function, start_idx: int = 1) -> typing.Tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


def get_default_args(func: Function) -> typing.Dict[str, typing.Any]:
    kwdefaults = func.__kwdefaults__
    if kwdefaults:
        return kwdefaults

    defaults = func.__defaults__
    if not defaults:
        return {}

    return {
        k: defaults[i]
        for i, k in enumerate(resolve_arg_names(func, start_idx=0)[-len(defaults) :])
    }


def magic_bundle(
    func: Function,
    kwargs: typing.Dict[str, typing.Any],
    *,
    start_idx: int = 1,
) -> typing.Dict[str, typing.Any]:
    return {
        **get_default_args(func),
        **{k: v for k, v in kwargs.items() if k in resolve_arg_names(func, start_idx)},
    }


__all__ = ("resolve_arg_names", "get_default_args", "magic_bundle")
