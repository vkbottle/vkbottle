from vkbottle.user import User, types
from vkbottle.api import Api
from vkbottle.rule import VBMLUserRule, AbstractUserRule
from vkbottle import TaskManager, Message, PhotoUploader
from googletrans import Translator
import threading
import os
from vbml import Pattern
import asyncio, time, random, os


user = User(os.environ["TOKEN"].split("-")[0], debug="DEBUG")
uploader = PhotoUploader(user, True)
translator = Translator()
QUEUE = []


@user.on.message_new(VBMLUserRule("python: <code>"))
async def wrapper(ans: types.Message, code):
    if ans.from_id == user.user_id:
        return eval(code)


# @user.on.message_new()
async def d(ans: types.Message):
    if ans.from_id != user.user_id:
        if ans.text:
            text = translator.translate(text=ans.text, dest="en").text
            os.system(f"say \"{text.strip('()')}\"",)
        await user.api.messages.markAsRead(
            start_message_id=ans.message_id, peer_id=ans.peer_id
        )
    else:
        text = translator.translate(text=ans.text, dest="en").text
        await user.api.messages.edit(
            message_id=ans.message_id,
            message=f"{text} ({ans.text})",
            peer_id=ans.peer_id,
        )


user.run_polling()
