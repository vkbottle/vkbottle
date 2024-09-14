import inspect
import types
import typing

Function = typing.Union[
    typing.Callable[..., typing.Any],
    types.FunctionType,
]


def resolve_arg_names(func: Function, start_idx: int = 1) -> typing.Tuple[str, ...]:
    return func.__code__.co_varnames[start_idx : func.__code__.co_argcount]


def get_default_args(func: Function) -> typing.Dict[str, typing.Any]:
    fspec = inspect.getfullargspec(func)
    return dict(zip(fspec.args[::-1], (fspec.defaults or ())[::-1]))


def magic_bundle(
    func: Function,
    kwargs: typing.Dict[str, typing.Any],
    *,
    start_idx: int = 1,
) -> typing.Dict[str, typing.Any]:
    names = resolve_arg_names(func, start_idx)
    args = get_default_args(func)
    args.update({k: v for k, v in kwargs.items() if k in names})
    return args
