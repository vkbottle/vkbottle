from typing import Iterable, Type

from vkbottle.api import ABCAPI
from vkbottle.http import AiohttpClient, SingleSessionManager
from vkbottle.modules import logger
from vkbottle.polling import ABCPolling, UserPolling

from .user import User


def user_run_multibot(user: User, apis: Iterable[ABCAPI], polling_type: Type[ABCPolling] = UserPolling):
    """ Add run_polling with polling constructed from derived apis
    :param user: User main instance (api is not required)
    :param apis: Iterable of apis
    :param polling_type: polling type to be ran
    """
    for i, api_instance in enumerate(apis):
        logger.debug(f"Connecting API (index: {i})")
        polling = polling_type().construct(api_instance)
        api_instance.http = SingleSessionManager(AiohttpClient)
        user.loop_wrapper.add_task(user.run_polling(custom_polling=polling))
    user.loop_wrapper.run_forever(user.loop)
