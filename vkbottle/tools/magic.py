from __future__ import annotations

import typing
from inspect import unwrap

Function = typing.Callable[..., typing.Any]

CONTEXT_NAMES: typing.Final = (
    "context",
    "ctx",
    "context_variables",
)


def _unwrap_callable(func: Function, /) -> Function | None:
    """Return the underlying __code__-bearing function.

    Handles plain/wrapped functions and callable instances (via their __call__).
    Returns None when the callable cannot be introspected this way (e.g. a
    functools.partial), so callers can degrade gracefully instead of crashing.
    """
    f = unwrap(func)
    try:
        if f.__code__:
            return f
    except AttributeError:
        pass
    try:
        call = type(f).__call__
        if call.__code__:
            return call
    except AttributeError:
        pass
    return None


def _resolve_arg_names(
    func: Function,
    /,
    *,
    start_idx: int,
    stop_idx: int,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    exclude = exclude or set()
    resolved = _unwrap_callable(func)
    if resolved is None:
        return ()
    varnames = resolved.__code__.co_varnames[start_idx:stop_idx]
    return tuple(name for name in varnames if name not in exclude)


def resolve_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    resolved = _unwrap_callable(func)
    if resolved is None:
        return ()
    code = resolved.__code__
    return _resolve_arg_names(
        resolved,
        start_idx=start_idx,
        stop_idx=code.co_argcount + code.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_kwonly_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    resolved = _unwrap_callable(func)
    if resolved is None:
        return ()
    code = resolved.__code__
    return _resolve_arg_names(
        resolved,
        start_idx=code.co_argcount + start_idx,
        stop_idx=code.co_argcount + code.co_kwonlyargcount,
        exclude=exclude,
    )


def resolve_posonly_arg_names(
    func: Function,
    /,
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> tuple[str, ...]:
    resolved = _unwrap_callable(func)
    if resolved is None:
        return ()
    return _resolve_arg_names(
        resolved,
        start_idx=start_idx,
        stop_idx=resolved.__code__.co_posonlyargcount,
        exclude=exclude,
    )


def get_default_args(func: Function, /) -> dict[str, typing.Any]:
    resolved = _unwrap_callable(func)
    if resolved is None:
        return {}
    defaults = resolved.__defaults__
    kwdefaults = {} if not resolved.__kwdefaults__ else resolved.__kwdefaults__.copy()
    if not defaults:
        return kwdefaults

    # __defaults__ map to the trailing *positional* params only; including keyword-only
    # names here would shift the defaults onto the wrong parameters.
    positional_names = _resolve_arg_names(
        resolved, start_idx=0, stop_idx=resolved.__code__.co_argcount
    )
    default_args = {k: defaults[i] for i, k in enumerate(positional_names[-len(defaults) :])}
    default_args.update(kwdefaults)
    return default_args


def magic_bundle(
    func: Function,
    kwargs: dict[str, typing.Any],
    *,
    start_idx: int = 1,
    exclude: set[str] | None = None,
) -> dict[str, typing.Any]:
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
    "get_default_args",
    "magic_bundle",
    "resolve_arg_names",
    "resolve_kwonly_arg_names",
    "resolve_posonly_arg_names",
)
