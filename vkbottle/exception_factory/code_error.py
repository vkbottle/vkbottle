from .abc import ABCExceptionFactory
import typing
import gc


class CodeErrorFactory(ABCExceptionFactory):
    """ Code error factory
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/exception-factory/exception-factory.md
    """

    @classmethod
    def __call__(
            cls, code: typing.Optional[int] = None, error_description: typing.Optional[str] = None
    ) -> typing.Union["ABCExceptionFactory", typing.Type["ABCExceptionFactory"]]:
        """ Interactively chooses the factory was called for: if error_description
        """
        if error_description is not None:
            return cls.exception_to_raise(code, error_description)
        return cls.exception_to_handle(code)

    @classmethod
    def exception_to_raise(cls, code: int, error_description: str) -> "ABCExceptionFactory":
        """ Returns an error with error code and error_description
        """
        exception_type = type(cls.generate_exc_classname(code), (cls,), {})
        return exception_type(code, error_description)

    @classmethod
    def exception_to_handle(cls, code: typing.Optional[int] = None) -> typing.Type["ABCExceptionFactory"]:
        """ Returns error type from garbage compiler storage with error code.
        If code is not specified returns self type to handle exception with any code """
        catch_exc_classname = cls.generate_exc_classname(code)

        for obj in gc.get_objects():
            if (
                obj.__class__.__name__ == catch_exc_classname
            ):
                return obj.__class__
        return type(catch_exc_classname, (cls,), {})

    @classmethod
    def generate_exc_classname(cls, code: int) -> str:
        """ Generates unique exception classname based on error code """
        return f"{cls.__name__}_{code}"
