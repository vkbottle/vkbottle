import typing
from abc import ABC, abstractmethod


class ABCExceptionFactory(ABC, Exception):
    """ Abstract Exception Factory
    Documentation: \
    https://github.com/timoniq/vkbottle/blob/master/docs/low-level/exception_factory/exception-factory.md
    """

    @classmethod
    @abstractmethod
    def __call__(
        cls, *args, **kwargs
    ) -> typing.Union["ABCExceptionFactory", typing.Type["ABCExceptionFactory"]]:
        pass

    @classmethod
    @abstractmethod
    def exception_to_raise(cls, *args, **kwargs) -> "ABCExceptionFactory":
        pass

    @classmethod
    @abstractmethod
    def exception_to_handle(cls, *args, **kwargs) -> typing.Type["ABCExceptionFactory"]:
        pass

    @classmethod
    @abstractmethod
    def generate_exc_classname(cls, *args, **kwargs) -> str:
        pass
