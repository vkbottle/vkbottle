from abc import ABC, abstractmethod
import typing


class ABCExceptionFactory(ABC, BaseException):
    """ Abstract Exception Factory
    Documentation: \
    https://github.com/timoniq/vkbottle/tree/v3.0/docs/exception-factory/exception-factory.md
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
