from typing import Dict, Type, TypeVar

T = TypeVar("T")


def cls_kwargs(cls: Type[T], kwargs: Dict[str, object]) -> T:
    return cls(**kwargs)


class ReducibleKwargsException(Exception):
    def __reduce__(self):
        return cls_kwargs, (self.__class__, self.__dict__)
