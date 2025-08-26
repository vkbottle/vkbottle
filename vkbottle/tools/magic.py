from __future__ import annotations

import typing

Function = typing.Callable[..., typing.Any]

CONTEXT_NAMES: typing.Final = (
    "context",
    "ctx",
    "context_variables",
)


def _resolve_arg_names(
    func: Function,
    /,
    *,
    start_idx: int,
    stop_idx: int,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    exclude = exclude or set()
    varnames = func.__code__.co_varnames[start_idx:stop_idx]
    return tuple(name for name in varnames if name not in exclude)


def resolve_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=start_idx,
        stop_idx=func.__code__.co_argcount + func.__code__.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_kwonly_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=func.__code__.co_argcount + start_idx,
        stop_idx=func.__code__.co_argcount + func.__code__.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_posonly_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    return _resolve_arg_names(
        func,
        start_idx=start_idx,
        stop_idx=func.__code__.co_posonlyargcount,
        exclude=exclude,
    )


def get_default_args(func: Function, /) -> typing.Dict[str, typing.Any]:
    defaults = func.__defaults__
    kwdefaults = {} if not func.__kwdefaults__ else func.__kwdefaults__.copy()
    if not defaults:
        return kwdefaults

    default_args = {
        k: defaults[i]
        for i, k in enumerate(resolve_arg_names(func, start_idx=0)[-len(defaults) :])
    }
    default_args.update(kwdefaults)
    return default_args


def magic_bundle(
    func: Function,
    kwargs: typing.Dict[str, typing.Any],
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> typing.Dict[str, typing.Any]:
    """This function returns a dictionary containing all default arguments of the function,
    merged with the provided keyword arguments.
    """
    arg_names = resolve_arg_names(func, start_idx=start_idx, exclude=exclude)
    default_args = get_default_args(func)
    default_args.update({k: v for k, v in kwargs.items() if k in arg_names})

    for name in CONTEXT_NAMES:
        if name in arg_names:
            default_args[name] = kwargs.copy()
            break

    return default_args


__all__ = (
    "magic_bundle",
    "get_default_args",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
)
