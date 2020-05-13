import typing
import traceback
from vkbottle.utils import logger


def swear(
    exception: typing.Union[Exception, typing.Tuple[Exception]],
    exception_handler: typing.Callable = None,
    ignore: bool = False,
) -> typing.Union[typing.Any, Exception]:
    """ Swear catcher allows to handle exceptions
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception as e:
                if ignore:
                    return e
                if exception_handler is not None:
                    await exception_handler(e, *args, **kwargs)
                else:
                    logger.error(traceback.format_exc())
            finally:
                logger.debug(f"{func.__name__} successfully handled with swear")

        return wrapper

    return decorator
