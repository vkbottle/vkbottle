from abc import ABCMeta
from typing import Any


class SingletonMeta(type):
    __instance__ = None

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls.__instance__ is None:
            cls.__instance__ = super().__call__(*args, **kwargs)
        return cls.__instance__


class ABCSingletonMeta(ABCMeta, SingletonMeta):
    pass


class ABCSingleton(metaclass=ABCSingletonMeta):
    pass


__all__ = ("ABCSingleton", "ABCSingletonMeta", "SingletonMeta")
