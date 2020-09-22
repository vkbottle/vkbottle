from vkbottle import Bot
from .blueprints import bps
import logging
import os

bot = Bot(os.environ["token"])
logging.basicConfig(level=logging.INFO)

for bp in bps:
    bp.load(bot)

bot.run_forever()
