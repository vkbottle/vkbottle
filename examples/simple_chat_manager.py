from vkbottle import Bot, Message
from vkbottle.rule import ChatActionRule

bot = Bot("token")


async def check(ans, id: int) -> bool:
    items = (await bot.api.messages.get_conversations_by_id(peer_ids=ans.peer_id)).items
    if not items:
        return False
    chat_settings = items[0].chat_settings
    admins = []
    admins.extend(chat_settings.admin_ids)
    admins.append(chat_settings.owner_id)
    return id in admins


async def getid(pattern: str) -> int:
    if pattern.isdigit():
        return pattern
    elif "vk.com/" in pattern:
        uid = (await bot.api.users.get(user_ids=pattern.split("/")[-1]))[0]
        return uid.id
    elif "[id" in pattern:
        uid = pattern.split("|")[0]
        return uid.replace("[id", "")


@bot.on.chat_invite()
async def chatstart(_):
    return "Привет! Для работы бота необходимо выдать права администратора"


@bot.on.chat_message(ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]))
async def invite(_):
    return "Приветствую в нашей беседе!"


@bot.on.chat_message(text=["кик", "kick", "kick <domain>", "кик <domain>"], lower=True)
async def kick(ans: Message, domain=""):
    if await getid(domain):
        user = await getid(domain)
    elif ans.reply_message:
        user = ans.reply_message.from_id
    else:
        return "Напиши ид или ответь на сообщение того, кого нужно исключить из чата"
    if not await check(ans, ans.from_id):
        return "Этой командой может воспользоваться только администратор"
    if user == bot.group_id:
        return "Вас что-то не устраивает?"
    if await check(ans, user):
        return "Я не могу исключить администратора беседы"

    await bot.api.messages.remove_chat_user(
        chat_id=ans.peer_id - 2000000000, member_id=user
    )


@bot.on.chat_message(ChatActionRule(["chat_kick_user"]))
async def chat_leave(ans: Message):
    if ans.action.member_id == ans.from_id:
        await bot.api.messages.remove_chat_user(
            chat_id=ans.peer_id - 2000000000, member_id=ans.action.member_id
        )
        return "Пользователь был исключен за выход из беседы."


@bot.on.chat_message(text=["everyone <text>", "everyone"], lower=True)
async def ping(ans, text="Сообщение не указано"):
    if not await check(ans, id=ans.from_id):
        return "Этой командой может воспользоваться только администратор"
    member_ids = (
        item.member_id
        for item in (
            await bot.api.messages.get_conversation_members(peer_id=ans.peer_id)
        ).items
        if item.member_id > 0 and item.member_id != ans.from_id
    )
    if member_ids is None:
        return "В вашей беседе нет участников"

    await ans(f"{text}{''.join(f'[id{member_id}| ]' for member_id in member_ids)}")


if __name__ == "__main__":
    bot.run_polling()
