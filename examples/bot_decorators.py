from vkbottle import Bot, Message

bot = Bot("token")


@bot.on.message(text=["hi", "hello"])
async def wrapper(ans: Message):
    # Works if message 'hi' or 'hello' in private dialog is received
    await ans("hi")


@bot.on.chat_message(text="banana")
async def wrapper(ans: Message):
    # Works if message 'banana' in chat received
    await ans("clean me..")


@bot.on.message_handler(text="apple")
async def wrapper(ans: Message):
    # Works if message 'apple' in both (chat or private) dialog received
    await ans("steve jobs..((((")


from vkbottle.types import GroupJoin


@bot.on.event.group_join()
async def wrapper(event: GroupJoin):
    print("User id{} just joined the group".format(event.user_id))


@bot.on.chat_action("chat_title_update")
async def wrapper(ans: Message):
    await ans("New chat name: {}".format(ans.action.text))


@bot.on.message("my name is <name>")
async def wrapper(ans: Message, name):
    await ans("your name is {}".format(name))


@bot.on.message(text="+<country_code:int>(<state_code:int>)<number:int>")
async def wrapper(ans: Message, country_code, state_code, number):
    return f"{country_code + 1}{state_code}{number}"


@bot.on.chat_invite()
async def wrapper(ans: Message):
    await ans("Hooray! Hi, friends!")


@bot.on.chat_mention()
async def wrapper(ans: Message):
    await ans("I was mentioned")


if __name__ == "__main__":
    bot.run_polling()
