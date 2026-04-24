from collections.abc import Iterable
from typing import TYPE_CHECKING, Type

from vkbottle.http import SingleAiohttpClient
from vkbottle.modules import logger
from vkbottle.polling import BotPolling
from vkbottle.tools._runner import run as _run

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.polling import ABCPolling

    from .bot import Bot


def run_multibot(
    bot: "Bot",
    apis: Iterable["ABCAPI"],
    polling_type: Type["ABCPolling"] = BotPolling,
):
    """Add run_polling with polling constructed from derived apis
    :param bot: Bot main instance (api is not required)
    :param apis: Iterable of apis
    :param polling_type: polling type to be ran
    """

    tasks = []
    for i, api_instance in enumerate(apis):
        logger.debug("Connecting API (index: {})", i)
        polling = polling_type().construct(api_instance)
        api_instance.http_client = SingleAiohttpClient()
        tasks.append(bot.run_polling(custom_polling=polling))

    _run(
        *bot.startup_tasks,
        *tasks,
        on_startup=bot.on_startup,
        on_shutdown=bot.on_shutdown,
    )
