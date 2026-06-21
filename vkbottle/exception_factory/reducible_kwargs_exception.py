from typing import Any, TypeVar

T = TypeVar("T")


def restore_exception(cls: type[T], args: tuple[Any, ...], state: dict[str, Any]) -> T:
    exc = cls.__new__(cls)
    exc.args = args
    exc.__dict__.update(state)
    return exc


class ReducibleKwargsException(Exception):
    def __reduce__(self):
        # Reconstruct directly from the stored state instead of re-running __init__:
        # the instance dict (e.g. request_params already normalized to a dict, plus a
        # `kwargs` attribute) does not match the __init__ signature, so calling
        # __init__ would raise TypeError and nest kwargs under a spurious key.
        return restore_exception, (self.__class__, self.args, self.__dict__)
