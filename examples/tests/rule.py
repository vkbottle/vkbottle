from vkbottle import Bot, Message
from vkbottle.rule import ChatActionRule, AttachmentRule
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug="DEBUG")


@bot.on.chat_message(ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]))
async def invite(ans: Message):
    await ans("Ура меня пригласили!", attachment="photo-189607270_457241022")


@bot.on.message_handler(AttachmentRule(["photo", "video"]))
async def pic(ans: Message):
    await ans("Какой чудесный котик на картинке <3")


@bot.on.message_handler(lev=["/бан", "/забанить"])
async def ban(ans: Message):
    if ans.reply_message:
        if ans.reply_message.from_id < 0:
            return "Не баню своих коллег..."

        person = (
            await bot.api.request(
                "users.get",
                {
                    "user_ids": ans.reply_message.from_id,
                    "name_case": "acc",
                    "fields": "sex",
                },
            )
        )[0]

        return (
            f"Я бы конечно забанил @id{ans.reply_message.from_id} ({person['first_name']}), но {'она' if person['sex'] == 1 else 'он'} милашка..😍🥰😇",
        )
    return "Ты забыл ответить на сообщение :("


bot.run_polling()
