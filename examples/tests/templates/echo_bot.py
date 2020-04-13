from vkbottle.framework.bot.templates.echo import Echo
from vkbottle import Bot
import os

bot = Bot(os.environ["TOKEN"], debug="DEBUG")
Echo(bot).ready().run()
