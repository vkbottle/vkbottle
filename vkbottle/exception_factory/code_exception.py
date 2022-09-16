from typing import Any, Dict, Optional, Tuple, TypeVar, Union, cast, overload

T = TypeVar("T", bound="CodeExceptionMeta")


class CodeExceptionMeta(type):
    code: int
    __exceptions__: Dict[int, Any]
    __code_specified__ = False

    def __init__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, object],
        *,
        code: Optional[int] = None,
    ):
        super().__init__(name, bases, attrs)
        if code is None:
            cls.__exceptions__ = {}

    def __call__(cls, *args: object, **kwargs: object) -> object:
        if not cls.__code_specified__:
            raise TypeError("exception code is not specified")
        return super().__call__(*args, **kwargs)

    @overload
    def __getitem__(cls: T, code: int, /) -> Union[T, Any]:
        ...

    @overload
    def __getitem__(cls: T, codes: Tuple[int, ...], /) -> Union[Tuple[T, ...], Any]:
        ...

    def __getitem__(
        cls: T,
        code_or_codes: Union[int, Tuple[int, ...]],
        /,
    ) -> Union[T, Tuple[T], Any]:
        if cls.__code_specified__:
            raise TypeError("exception code already specified")
        if isinstance(code_or_codes, tuple):
            return tuple(cls._get_exception(code) for code in code_or_codes)
        return cls._get_exception(code_or_codes)

    def register_exception(cls: T, exception: T, code: int) -> None:
        exception.code = code
        exception.__code_specified__ = True
        cls.__exceptions__[code] = exception

    def _get_exception(cls: T, code: int) -> T:
        if code not in cls.__exceptions__:
            cls._create_exception(code)
        return cls.__exceptions__[code]

    def _create_exception(cls, code: int) -> None:
        cls.register_exception(
            cast(CodeExceptionMeta, type(f"{cls.__name__}_{code}", (cast(type, cls),), {})), code
        )


class CodeException(Exception, metaclass=CodeExceptionMeta):
    code: int

    def __init_subclass__(cls, code: Optional[int] = None, **kwargs: object) -> None:
        if code is not None:
            cls.register_exception(cls, code)
