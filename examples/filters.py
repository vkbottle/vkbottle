from vkbottle import Bot, Message
from vkbottle.rule import filters, PayloadRule, CommandRule, AttachmentRule

bot = Bot("token")


@bot.on.message_handler(
    filters.or_filter(PayloadRule({"command": "look"}),
                      CommandRule(["смотри", "look"])),
    AttachmentRule(["photo"]),
)
async def wrapper(ans: Message):
    await ans("Да, фильтры работают!")


if __name__ == "__main__":
    bot.run_polling()
