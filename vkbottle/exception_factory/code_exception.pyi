from typing import (
    ClassVar,
    Dict,
    Optional,
    Tuple,
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
        cls: T_CodeExceptionMeta, code_or_codes: Tuple[int, ...]
    ) -> Tuple[T_CodeExceptionMeta, ...]: ...

class CodeException(Exception, metaclass=_CodeExceptionMeta):
    code: ClassVar[int]

    def __init_subclass__(cls, code: Optional[int] = None, **kwargs: Dict[str, object]): ...
