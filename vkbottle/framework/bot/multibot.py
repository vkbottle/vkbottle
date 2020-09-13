from .bot import Bot
from vkbottle.api import ABCAPI
from vkbottle.polling import ABCPolling, BotPolling
from typing import Iterable, Type
from vkbottle.http import SingleSessionManager, AiohttpClient


def run_multibot(bot: Bot, apis: Iterable[ABCAPI], polling_type: Type[ABCPolling] = BotPolling):
    """ Add run_polling with polling constructed from derived apis
    :param bot: Bot main instance (api is not required)
    :param apis: Iterable of apis
    :param polling_type: polling type to be ran
    """
    for api_instance in apis:
        polling = polling_type().construct(api_instance)
        api_instance.http = SingleSessionManager(AiohttpClient)
        bot.loop_wrapper.add_task(bot.run_polling(custom_polling=polling))
    bot.loop_wrapper.run_forever(bot.loop)
