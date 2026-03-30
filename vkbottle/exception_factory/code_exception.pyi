from typing import (
    Any,
    ClassVar,
    TypeVar,
    overload,
)

T_CodeExceptionMeta = TypeVar("T_CodeExceptionMeta", bound="_CodeExceptionMeta")

T_CodeException = TypeVar("T_CodeException", bound="CodeException")

class _CodeExceptionMeta(type):
    code: int

    @overload
    def __getitem__(cls: T_CodeExceptionMeta, code_or_codes: int) -> T_CodeExceptionMeta: ...
    @overload
    def __getitem__(
        cls: T_CodeExceptionMeta, code_or_codes: tuple[int, ...]
    ) -> tuple[T_CodeExceptionMeta, ...]: ...

class CodeException(Exception, metaclass=_CodeExceptionMeta):
    code: ClassVar[int]

    def __init_subclass__(cls, code: int | None = None, **kwargs: Any) -> None: ...
