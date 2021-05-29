import gc
import typing

from .abc import ABCExceptionFactory


class CodeErrorFactory(ABCExceptionFactory):
    """ Code error factory
    Documentation: \
    https://github.com/timoniq/vkbottle/blob/master/docs/low-level/exception_factory/exception-factory.md
    """

    def __init__(
        self,
        code: typing.Optional[int] = None,
        error_description: typing.Optional[str] = None,
        raw_error: typing.Optional[dict] = None,
    ):
        self.code = code
        self.error_description = error_description
        self.raw_error = raw_error

    @classmethod
    def __call__(  # type: ignore
        cls,
        code: typing.Optional[int] = None,
        error_description: typing.Optional[str] = None,
        raw_error: typing.Optional[dict] = None,
    ) -> typing.Union["ABCExceptionFactory", typing.Type["ABCExceptionFactory"]]:
        """ Interactively chooses the factory was called for: if error_description
        """
        if error_description is not None:
            return cls.exception_to_raise(code, error_description, raw_error)  # type: ignore
        return cls.exception_to_handle(code)

    @classmethod
    def exception_to_raise(  # type: ignore
        cls, code: int, error_description: str, raw_error: dict
    ) -> "ABCExceptionFactory":
        """ Returns an error with error code and error_description
        """
        exception_type = type(cls.generate_exc_classname(code), (cls,), {})
        return exception_type(code, error_description, raw_error)

    @classmethod
    def exception_to_handle(  # type: ignore
        cls, code: typing.Optional[int] = None
    ) -> typing.Type["ABCExceptionFactory"]:
        """ Returns error type from garbage compiler storage with error code.
        If code is not specified returns self type to handle exception with any code """
        if code is None:
            return cls

        catch_exc_classname = cls.generate_exc_classname(code)

        for obj in gc.get_objects():
            if obj.__class__.__name__ == catch_exc_classname:
                return obj.__class__

        return type(catch_exc_classname, (cls,), {})

    @classmethod
    def generate_exc_classname(cls, code: typing.Optional[int]) -> str:  # type: ignore
        """ Generates unique exception classname based on error code """
        return f"{cls.__name__}_{code}"

    def __str__(self):
        return f"[{self.code}] {self.error_description}\n"
