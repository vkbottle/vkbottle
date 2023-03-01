import sys
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Generic,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

if TYPE_CHECKING:
    from types import ModuleType


T_CodeExceptionMeta = TypeVar("T_CodeExceptionMeta", bound="CodeExceptionMeta")

T_CodeException = TypeVar("T_CodeException", bound="CodeException")


if TYPE_CHECKING:

    class CodeExceptionMeta(type):
        code: int

        @overload
        def __getitem__(cls: T_CodeExceptionMeta, code_or_codes: int) -> T_CodeExceptionMeta:
            ...

        @overload
        def __getitem__(
            cls: T_CodeExceptionMeta, code_or_codes: Tuple[int, ...]
        ) -> Tuple[T_CodeExceptionMeta, ...]:
            ...

        def __getitem__(
            cls: T_CodeExceptionMeta, code_or_codes: Union[int, Tuple[int, ...]]
        ) -> Union[T_CodeExceptionMeta, Tuple[T_CodeExceptionMeta, ...]]:
            ...

    class CodeException(Exception, metaclass=CodeExceptionMeta):
        code: ClassVar[int]

        def __init_subclass__(cls, code: Optional[int] = None, **kwargs: Dict[str, object]):
            ...

else:

    class CodeException(Exception):
        code: ClassVar[int]

        def __init_subclass__(cls, code: Optional[int] = None, **kwargs: Dict[str, object]):
            super().__init_subclass__(**kwargs)
            if code is not None:
                cls.code = code
                for base in cls.mro()[1:]:
                    if issubclass(base, CodeException):
                        sys.modules[base.__module__].__dict__[f"{base.__name__}_{code}"] = cls
                        break

        @overload
        def __class_getitem__(
            cls: Type[T_CodeException], code_or_codes: int
        ) -> Type[T_CodeException]:
            ...

        @overload
        def __class_getitem__(
            cls: Type[T_CodeException], code_or_codes: Tuple[int, ...]
        ) -> Tuple[Type[T_CodeException], ...]:
            ...

        def __class_getitem__(
            cls: Type[T_CodeException], code_or_codes: Union[int, Tuple[int, ...]]
        ) -> Union[Type[T_CodeException], Tuple[Type[T_CodeException], ...]]:
            if isinstance(code_or_codes, int):
                return get_code_exception(cls, code_or_codes)
            return tuple(get_code_exception(cls, code) for code in code_or_codes)


def get_code_exception(cls: Type[T_CodeException], code: int) -> Type[T_CodeException]:
    return CodeExceptionFactory(cls, code).get()


class CodeExceptionFactory(Generic[T_CodeException]):
    def __init__(self, cls: Type[T_CodeException], code: int):
        self._class = cls
        self._code = code

    def get(self) -> Type[T_CodeException]:
        if not self._code_exists:
            self._create_code_exception()
        return self._code_exception

    @property
    def _code_exists(self) -> bool:
        return self._code_exception_name in self._base_class_namespace

    def _create_code_exception(self) -> None:
        code_exception: Type[CodeException] = type(
            self._code_exception_name, (self._class,), {"__module__": self._class.__module__}
        )
        code_exception.code = self._code
        self._base_class_namespace[self._code_exception_name] = code_exception

    @property
    def _code_exception(self) -> Type[T_CodeException]:
        return self._base_class_namespace[self._code_exception_name]

    @property
    def _code_exception_name(self) -> str:
        return f"{self._class.__name__}_{self._code}"

    @property
    def _base_class_namespace(self) -> Dict[str, Any]:
        return self._base_class_module.__dict__

    @property
    def _base_class_module(self) -> "ModuleType":
        return sys.modules[self._class.__module__]
