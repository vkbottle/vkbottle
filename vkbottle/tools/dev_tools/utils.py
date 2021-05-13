import importlib
import os
import re
import typing
import asyncio

from vkbottle.api.token_generator.consistent import ConsistentTokenGenerator
from vkbottle.api.token_generator.single import SingleTokenGenerator
from vkbottle.dispatch.filter import AndFilter, OrFilter
from vkbottle.dispatch.rules import ABCRule

if typing.TYPE_CHECKING:
    from vkbottle.framework.abc_blueprint import ABCBlueprint
    from vkbottle.api.token_generator import ABCTokenGenerator, Token


# This feature is not used in production
# but can be useful for customization
# purposes
def run_in_task(coroutine: typing.Coroutine) -> None:
    """ Gets loop and runs add makes task from the given coroutine """
    loop = asyncio.get_running_loop()
    loop.create_task(coroutine)


def convert_shorten_filter(
    shorten: typing.Union[ABCRule, typing.Tuple[ABCRule, ...], typing.Set[ABCRule]]
) -> "ABCRule":
    """ Shortener. Converts tuple/list of rules to OrFilter and set of rules to AndFilter
    :param shorten: list/tuple/set of rules or a single rule
    """
    if isinstance(shorten, set):
        return AndFilter(*shorten)
    elif isinstance(shorten, tuple):
        return OrFilter(*shorten)
    return shorten


def load_blueprints_from_package(package_name: str) -> typing.Iterator["ABCBlueprint"]:
    """ Gets blueprints from package
    >>> for bp in load_blueprints_from_package("blueprints"):
    >>>     bp.load(...)
    """
    bp_paths = []
    for filename in os.listdir(package_name):
        if filename.startswith("__"):
            continue
        elif not filename.endswith(".py"):
            yield from load_blueprints_from_package(os.path.join(package_name, filename))
            continue

        with open(os.path.join(package_name, filename)) as file:
            bp_names = re.findall(
                r"^(\w+) = (?:Bot|User|)Blueprint\(", file.read(), flags=re.MULTILINE
            )
            assert len(bp_names) == 1
            bp_paths.append((filename[:-3], bp_names[0]))

    for bp_path in bp_paths:
        module, bp_name = bp_path
        module_name = package_name.replace("." + os.sep, ".").replace(os.sep, ".")
        bp_module = importlib.import_module(module_name + "." + module)
        yield getattr(bp_module, bp_name)
