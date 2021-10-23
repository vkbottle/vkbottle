from typing import Callable
import inspect


def get_acceptable_kwargs(func: Callable, context: dict) -> dict:
    signature = inspect.signature(func)
    if inspect.Parameter.VAR_KEYWORD in signature.parameters.values():
        return context
    acceptable_keys = list(signature.parameters.keys())[1:]
    return {k: v for k, v in context.items() if k in acceptable_keys}
