from vkbottle import Bot, Message
from vkbottle import carousel_gen, CarouselEl, keyboard_gen
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])

template = carousel_gen(
    CarouselEl(
        photo_id="-109837093_457242809",
        buttons=keyboard_gen([[{"text": "баттон 1"}]]),
        action={"type": "open_photo"}
    ),
    CarouselEl(
        photo_id="-109837093_457242809",
        buttons=keyboard_gen([[{"text": "баттон 2"}]]),
        action={"type": "open_photo"}
    ),
)

@bot.on.message_handler(text="хочу темплейт", lower=True)
async def consignment(ans: Message):
    await ans(ans.dict())
    await ans("Держи темплейт!", template=template)


bot.run_polling()
