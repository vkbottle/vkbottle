from .abc import ABCExceptionFactory
import typing


class SingleError(ABCExceptionFactory):
    """ Single error factory
    Documentation: \
    https://github.com/timoniq/vkbottle/tree/v3.0/docs/exception-factory/exception-factory.md
    """

    @classmethod
    def __call__(cls, exception_description: str) -> "ABCExceptionFactory":  # type: ignore
        """ Returns an exception to raise
        """
        return cls.exception_to_raise(exception_description)

    @classmethod
    def exception_to_raise(  # type: ignore
        cls, exception_description: str
    ) -> "ABCExceptionFactory":
        """ Returns an exception to raise
        """
        return cls(exception_description)

    @classmethod
    def exception_to_handle(  # type: ignore
        cls, code: typing.Optional[int] = None
    ) -> typing.Type["ABCExceptionFactory"]:
        """ Returns exception class """
        return cls

    @classmethod
    def generate_exc_classname(cls) -> str:  # type: ignore
        return cls.__name__
