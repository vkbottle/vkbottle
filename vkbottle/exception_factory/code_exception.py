from typing import TYPE_CHECKING, Any, Dict, Tuple, Type, TypeVar, Union, overload

T = TypeVar("T", bound="CodeExceptionMeta")


class CodeExceptionMeta(type):
    def __init__(cls: T, name: str, bases: Tuple[Type[Any], ...], attrs: Dict[str, Any]):
        super().__init__(name, bases, attrs)
        cls.code: int
        cls.__exceptions__: Dict[int, T] = {}
        cls.__code_specified__ = False

    def __call__(cls: T, *args: Any, **kwargs: Any) -> Any:
        if cls.__code_specified__ is False:
            raise TypeError("exception code is not specified")

        return super().__call__(*args, **kwargs)

    @overload
    def __getitem__(cls: T, code: int) -> T:
        ...

    @overload
    def __getitem__(cls: T, code: Tuple[int, ...]) -> Tuple[T, ...]:
        ...

    def __getitem__(cls: T, code: Union[int, Tuple[int, ...]]) -> Union[T, Tuple[T, ...]]:
        if cls.__code_specified__ is True:
            raise TypeError("exception code already specified")

        if isinstance(code, tuple):
            return tuple(cls._get_exception(c) for c in code)

        return cls._get_exception(code)

    def _get_exception(cls: T, code: int) -> T:
        if code in cls.__exceptions__:
            return cls.__exceptions__[code]

        return cls._register_exception(code)

    def _register_exception(cls: T, code: int) -> T:
        name = f"{cls.__name__}_{code}"
        exception = cls.__class__(name, (cls,), dict(cls.__dict__))

        exception.code = code
        exception.__code_specified__ = True
        cls.__exceptions__[code] = exception

        return exception


class CodeException(Exception, metaclass=CodeExceptionMeta):
    if TYPE_CHECKING:
        code: int
