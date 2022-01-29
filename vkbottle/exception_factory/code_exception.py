from typing import Dict, Tuple, Type, TypeVar, Union, cast, no_type_check, overload

T = TypeVar("T", bound=Type["CodeException"])


class CodeException(Exception):
    code: int
    __code_specified__: bool = False
    __exceptions__: Dict[int, Type["CodeException"]] = {}

    @no_type_check
    def __new__(cls, *args, **kwargs):
        if not cls.__code_specified__:
            raise TypeError("exception code is not specified")

        return super().__new__(cls, *args, **kwargs)

    @no_type_check
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__exceptions__ = {}

    @overload
    def __class_getitem__(cls: T, code: int) -> T:
        ...

    @overload
    def __class_getitem__(cls: T, code: Tuple[int, ...]) -> Tuple[T, ...]:
        ...

    def __class_getitem__(cls: T, code: Union[int, Tuple[int, ...]]) -> Union[T, Tuple[T, ...]]:
        if cls.__code_specified__:
            raise TypeError("exception code already specified")

        if isinstance(code, tuple):
            return tuple(cls._get_exception(c) for c in code)

        return cls._get_exception(code)

    @classmethod
    def _get_exception(cls: T, code: int) -> T:
        if code in cls.__exceptions__:
            return cast(T, cls.__exceptions__[code])

        return cls._register_exception(code)

    @classmethod
    def _register_exception(cls: T, code: int) -> T:
        name = f"{cls.__name__}_{code}"
        exception = cast(T, type(name, (cls,), {}))  # type: ignore

        exception.code = code
        exception.__code_specified__ = True
        cls.__exceptions__[code] = exception

        return exception
