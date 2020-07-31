import typing
import traceback
from vkbottle.utils import logger


def swear(
    exception: typing.Union[Exception, typing.Tuple[Exception]],
    exception_handler: typing.Callable = None,
    ignore: bool = False,
    just_log: bool = False,
) -> typing.Union[typing.Any, Exception]:
    """ Swear catcher allows to handle exceptions | Used as a decorator
    :param exception: Exception(s) to handle
    :param exception_handler: async exception handler
    :param ignore: should the exception be ignored
    :param just_log: should swear handler log the error

    >>> @swear(RuntimeError, ignore=True)
    >>> async def function():
    >>>     raise RuntimeError("Oh no!")
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception as e:
                if ignore:
                    return e
                if exception_handler is not None:
                    return await exception_handler(e, *args, **kwargs)
                elif just_log:
                    logger.error(
                        "While {func} was handling error occurred \n\n{traceback}",
                        func=func.__name__,
                        traceback=traceback.format_exc(),
                    )
                return
            finally:
                logger.debug(f"{func.__name__} successfully handled with swear")

        return wrapper

    return decorator


throws = swear
