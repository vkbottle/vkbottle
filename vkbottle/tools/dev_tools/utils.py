from asyncio import get_running_loop
from typing import Coroutine, NoReturn, Union, Tuple, Set
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.filter import AndFilter, OrFilter


# This feature is not used in production
# but can be useful for customization
# purposes
def run_in_task(coroutine: Coroutine) -> NoReturn:
    """ Gets loop and runs add makes task from the given coroutine """
    loop = get_running_loop()
    loop.create_task(coroutine)


def convert_shorten_filter(shorten: Union[ABCRule, Tuple[ABCRule, ...], Set[ABCRule]]):
    """ Shortener. Converts tuple/list of rules to OrFilter and set of rules to AndFilter
    :param shorten: list/tuple/set of rules or a single rule
    """
    if isinstance(shorten, set):
        return AndFilter(*shorten)
    elif isinstance(shorten, tuple):
        return OrFilter(*shorten)
    return shorten
