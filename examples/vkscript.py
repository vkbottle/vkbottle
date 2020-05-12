from vkbottle import Bot, Message, vkscript
from typing import List

bot = Bot("token")

@vkscript
def get_names(api, user_ids=1):
    names = []
    for user in api.users.get(user_ids=user_ids):
        names.append(user.first_name)
    return names


@bot.on.message_handler("/names <( )*ids:int>")
async def fetch_names(ans: Message, ids: List[int]):
    return ", ".join(await bot.api.execute(get_names(user_ids=ids)))

bot.run_polling()
