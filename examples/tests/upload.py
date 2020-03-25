from vkbottle import PhotoUploader, DocUploader, Bot, Message, User, TaskManager
from vkbottle.rule import VBMLUserRule
import os

bot = Bot(os.environ["TOKEN"], log_to_path=True)
user = User(os.environ["USER"])
photo_uploader = PhotoUploader(user, generate_attachment_strings=True)
doc_uploader = DocUploader(bot, generate_attachment_strings=True)


# PHOTOS
@bot.on.message(lev="upload photo to album")
async def upload_album(ans: Message):
    photo = await photo_uploader.upload_photo_to_album(
        269249589, "vkbottle_bot/img/1.jpg", bot.group_id
    )
    await ans("Okay,", photo)


@bot.on.message(lev=["post photo", "post photo to the wall"])
async def post(ans: Message):
    photo = await photo_uploader.upload_wall_photo("vkbottle_bot/img/1.jpg")
    await user.api.request(
        "wall.post",
        {"owner_id": -bot.group_id, "message": "лол тест", "attachments": photo},
    )
    return "Done!"


@bot.on.message(lev="main photo")
async def main(ans: Message):
    await photo_uploader.update_favicon("vkbottle_bot/img/1.jpg", bot.group_id)
    return "Done!"


@bot.on.message(lev="upload photo")
async def upload(ans: Message):
    photo = await photo_uploader.client(bot).upload_message_photo("vkbottle_bot/img/1.jpg")
    await ans("hipster?", photo)


@user.on.message_new(VBMLUserRule("chat favicon"))
async def chat_favicon(ans: Message):
    photo = await photo_uploader.upload_chat_favicon(
        "vkbottle_bot/img/1.jpg", chat_id=ans.chat_id
    )
    await user.api.request("messages.setChatPhoto", {"file": photo})
    return "yup!"


# DOCUMENTS
@bot.on.message(text="upload doc")
async def upload_doc(ans: Message):
    doc = await doc_uploader.upload_doc_to_message("vkbottle_bot/img/2.txt", ans.peer_id)
    await ans("take it", attachment=doc)


tm = TaskManager()
tm.add_task(bot.run(True))
tm.add_task(user.run)
tm.run()
