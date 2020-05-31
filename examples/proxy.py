from vkbottle import Proxy, Bot
from vkbottle.framework.bot.templates.echo import Echo
import os

proxy = Proxy(address="http://163.172.189.32:8811")
bot = Bot(os.environ["token"])

Echo(bot).ready().run()
