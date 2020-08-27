from .abc import ABCExceptionFactory
import typing


class SingleError(ABCExceptionFactory):
    """ Sinle error factory
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/exception-factory/exception-factory.md
    """

    @classmethod
    def __call__(cls, exception_description: str) -> typing.Type["ABCExceptionFactory"]:
        """ Returns an exception to raise
        """
        return cls.exception_to_raise(exception_description)

    @classmethod
    def exception_to_raise(cls, exception_description: str) -> "ABCExceptionFactory":
        """ Returns an exception to raise
        """
        return cls(exception_description)

    @classmethod
    def exception_to_handle(
        cls, code: typing.Optional[int] = None
    ) -> typing.Type["ABCExceptionFactory"]:
        """ Returns exception class """
        return cls

    @classmethod
    def generate_exc_classname(cls) -> str:
        return cls.__name__
