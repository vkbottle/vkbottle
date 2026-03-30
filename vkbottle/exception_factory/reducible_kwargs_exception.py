from typing import Any, TypeVar

T = TypeVar("T")


def cls_kwargs(cls: type[T], kwargs: dict[str, Any]) -> T:
    return cls(**kwargs)


class ReducibleKwargsException(Exception):
    def __reduce__(self):
        return cls_kwargs, (self.__class__, self.__dict__)
