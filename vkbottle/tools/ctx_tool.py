from typing import Any

try:
    import contextvars
except ImportError:
    contextvars = None  # type: ignore


class BaseContext:
    """Parent BaseContext class. Idea taken from aiogram"""

    ctx_instance: Any

    def __init_subclass__(cls, **kwargs):
        if not contextvars:
            raise LookupError(f"To use {cls.__name__} you have to install contextvars")

        cls.ctx_instance = contextvars.ContextVar(kwargs.get("ctx_name") or cls.__name__)
        return cls

    @classmethod
    def get_instance(cls, no_error: bool = True) -> Any:
        if no_error:
            return cls.ctx_instance.get(None)
        return cls.ctx_instance.get()

    @classmethod
    def set_instance(cls, value: Any) -> None:
        cls.ctx_instance.set(value)
