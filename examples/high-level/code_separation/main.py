import os

from vkbottle import Bot

from .handlers import labelers

bot = Bot(os.environ["token"])

for labeler in labelers:
    bot.labeler.load(labeler)

bot.run_forever()
