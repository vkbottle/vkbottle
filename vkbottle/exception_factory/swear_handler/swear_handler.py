import traceback
from inspect import iscoroutinefunction
from typing import Any, Callable, Optional, Tuple, Type, Union

from vkbottle.modules import logger

EXCEPTION = Union[Exception, Type[Exception]]


def swear(
    exception: Union[EXCEPTION, Tuple[EXCEPTION, ...]],
    exception_handler: Optional[Callable] = None,
    just_log: bool = False,
    just_return: bool = False,
) -> Any:
    """Swear catcher allows to handle exceptions | Used as a decorator
    :param exception: Exception(s) to handle
    :param exception_handler: async exception handler
    :param just_log: should swear handler log the error
    :param just_return: should the exception just be returned
    >>> @swear(RuntimeError, just_return=True)
    >>> def function():
    >>>     raise RuntimeError("Oh no!")
    >>> function()
    >>> RuntimeError("Oh no!")
    """

    if not isinstance(exception, tuple):
        exception = (exception,)

    def decorator(func: Callable):
        async def asynchronous_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception as e:
                if exception_handler is not None:
                    return await exception_handler(e, *args, **kwargs)
                elif just_log:
                    logger.error(
                        "{} (handling with swear) has thrown an exception: \n\n{}",
                        func.__name__,
                        traceback.format_exc(),
                    )
                elif just_return:
                    return e
            finally:
                logger.debug("Function {} was handled with swear", func.__name__)

        def synchronous_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                if exception_handler is not None:
                    return exception_handler(e, *args, **kwargs)
                elif just_log:
                    logger.error(
                        "{} (handling with swear) has thrown an exception: \n\n{}",
                        func.__name__,
                        traceback.format_exc(),
                    )
                elif just_return:
                    return e
            finally:
                logger.debug("Function {} was handled with swear", func.__name__)

        if iscoroutinefunction(func) and iscoroutinefunction(exception_handler):
            return asynchronous_wrapper
        return synchronous_wrapper

    return decorator
