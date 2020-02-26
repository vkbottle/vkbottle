from vkbottle import PhotoUploader, Bot, Message, User, TaskManager
from vkbottle.rule import VBMLUserRule
import os

bot = Bot(os.environ["TOKEN"], log_to_path=True)
user = User(os.environ["USER"])
user.mode(2)
uploader = PhotoUploader(user, generate_attachment_strings=True)


@bot.on.message(lev="upload album")
async def upload_album(ans: Message):
    photo = await uploader.upload_photo_to_album(
        269249589, "vkbottle_bot/img/1.jpg", bot.group_id
    )
    await ans("Okay,", photo)


@bot.on.message(lev=["post", "post on wall"])
async def post(ans: Message):
    photo = await uploader.upload_wall_photo("vkbottle_bot/img/1.jpg")
    await user.api.request(
        "wall.post",
        {"owner_id": -bot.group_id, "message": "лол тест", "attachments": photo},
    )
    return "Done!"


@bot.on.message(lev="main photo")
async def main(ans: Message):
    await uploader.update_favicon("vkbottle_bot/img/1.jpg", bot.group_id)
    return "Done!"


@bot.on.message(lev="upload")
async def upload(ans: Message):
    photo = await uploader.client(bot).upload_message_photo("vkbottle_bot/img/1.jpg")
    await ans("hipster?", photo)


@user.on.message_new(VBMLUserRule("chat favicon"))
async def chat_favicon(ans: Message):
    photo = await uploader.upload_chat_favicon(
        "vkbottle_bot/img/1.jpg", chat_id=ans.chat_id
    )
    await user.api.request("messages.setChatPhoto", {"file": photo})
    return "ура"


tm = TaskManager()
tm.add_task(bot.run)
tm.add_task(user.run)
tm.run()
