# Bot-Labeler

Удобная оболочка над роутерами. С помощью лейблера создаются хендлеры. Может быть использовано в качестве портабельного диспатчера.

Имеет метод load который должен загружать хендлеры и мидлвари в текущий лейблер из переданного. Может быть использовано для разбивания кода на много частей.

## Пример

### bot.py

```python
from vkbottle import Bot
from routes import labelers

bot = Bot("token")

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()
```

### routes/\_\_init\_\_.py

```python
from . import greetings, goodbyes

labelers = [greetings.bl, goodbyes.bl]
```

### routes/greetings.py

```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["привет", "хай", "здравствуй"])
async def greeting(message: Message):
    await message.answer("Привет, друг")
```

### routes/goodbyes.py

```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["пока", "до свидания"])
async def greeting(message: Message):
    await message.answer("До новых встреч")
```
