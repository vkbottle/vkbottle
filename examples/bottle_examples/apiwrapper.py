from vkbottler.vkbottle import Bot, Message

bot = Bot('token', 1, debug=True, plugin_folder='examplebot')

# Answer <Ты FIRST_NAME LAST_NAME. Статус по жизни: «STATUS». У тебя публичный(IS_CLOSED)закрытый профиль> to <!кто я>
@bot.on.message.lower('!кто я')
async def wrapper(ans: Message):
    user = (await bot.api.users.get(user_ids=ans.from_id, fields=','.join(['status', 'photo_id'])))[0]
    await ans(f'Ты {user["first_name"]} {user["last_name"]}. Статус по жизни: <<{user["status"]}>>. '
              f'У тебя {"публичный" if not user["is_closed"] else "закрытый"} профиль!',
              attachment=f'photo-{user["photo_id"]}')

bot.run_polling()
