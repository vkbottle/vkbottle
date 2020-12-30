import os

from vkbottle import Keyboard, TemplateElement, Text, template_gen
from vkbottle.bot import Bot, Message

bot = Bot(os.environ["TOKEN"])


# You can use keyboard generators to fill the buttons field
keyboard_1 = Keyboard().add(Text("button 1", {})).get_json()
keyboard_2 = Keyboard().add(Text("button 2", {})).get_json()

# More about combining fields can be read in vk documentation
# for templates: https://vk.com/dev/bot_docs_templates
template = template_gen(
    TemplateElement(
        photo_id="-109837093_457242809",
        buttons=keyboard_1,
        action={"type": "open_photo"}
    ),
    TemplateElement(
        photo_id="-109837093_457242809",
        buttons=keyboard_2,
        action={"type": "open_photo"}
    ),
)

@bot.on.message(text="хочу темплейт")
async def template_handler(message: Message):
    await message.answer("держи", template=template)

bot.run_forever()
