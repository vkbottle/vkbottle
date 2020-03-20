from vkbottle import Bot, Message
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])


@bot.on.message_handler(text={"<!>шуе<!>": "ппш", "<!>ппш<!>": "шпш"}, lower=True)
async def consignment(ans: Message, response: str):
    await ans(response)

bot.run_polling()
