from .handler.middleware import Middleware
from .framework import Bot
import glob, importlib, os


def concatenate_blueprint_from_dir(bot: Bot, dirname: str, dp: str = "dp"):
    all_list = list()
    for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            all_list.append(os.path.basename(f)[:-3])

    dispatcher = [importlib.import_module(dirname + "." + m, __package__) for m in all_list]
    for module in dispatcher:
        bot.on.concatenate(getattr(module, dp))

    return bot, dispatcher
