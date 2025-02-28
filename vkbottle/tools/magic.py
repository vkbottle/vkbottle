import typing

Function = typing.Callable[..., typing.Any]


def resolve_arg_names(func: Function, start_idx: int = 1) -> typing.Tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


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
) -> typing.Dict[str, typing.Any]:
    """This function returns a dictionary containing all default arguments of the function,
    merged with the provided keyword arguments.
    """
    arg_names = resolve_arg_names(func, start_idx)
    default_args = get_default_args(func)
    default_args.update({k: v for k, v in kwargs.items() if k in arg_names})
    return default_args


__all__ = ("resolve_arg_names", "get_default_args", "magic_bundle")
