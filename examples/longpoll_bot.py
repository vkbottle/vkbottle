from vkbottle import Bot, Message, keyboard_gen, types

bot = Bot("token")


@bot.on.message(text=["hi", "hello"])
async def wrapper(ans: Message):
    keyboard = [[{"text": "fantastic button"}]]
    await ans("hi, my lil friend", keyboard=keyboard_gen(keyboard))


@bot.on.event.group_join()
async def wrapper(event: types.GroupJoin):
    await bot.api.messages.send(
        peer_id=event.user_id, random_id=100, message="Welcome to the group!"
    )


@bot.error_handler(901, 902)
async def error(error):
    print("Cant send message to the user :(, error code:", error[0])


if __name__ == "__main__":
    bot.run_polling()
