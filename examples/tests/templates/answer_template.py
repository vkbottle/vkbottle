from vkbottle.framework.bot.templates.answer import Answer
import os

Answer(os.environ["TOKEN"]).ready("привет", "приветик :)").ready(
    "пока", "до свидания"
).run()
