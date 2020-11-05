from vkbottle import Bot
from .blueprints import bps
import logging
import os

# You should provide API to bot before
# constructing blueprints otherwise they won't
# have it, API is not needed if you are not
# requested to use it outside of handlers and
# cannot be passed to blueprint if you use
# multibot. Read the docs at
# > high-level/bot/blueprint
bot = Bot(os.environ["token"])
logging.basicConfig(level=logging.INFO)

for bp in bps:
    bp.load(bot)

bot.run_forever()
