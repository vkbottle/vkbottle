from vkbottle.framework.bot.templates.echo import Echo
import os

Echo(os.environ["TOKEN"]).ready().run()
