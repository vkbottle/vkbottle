# Waiter Machine

Waiter Machine для создания быстрых воронок без потери скоупа.

Таким образом с его помощью можно реализовать быстрые стейты и написать простейшие воронки.

В отличии от State Dispenser, состояния никуда не сериализуются, поэтому Waiter Machine не следует использовать для сложных стейтов, где важна консистентность проведения например транзакции или они активны долгое время.

Простейший пример с waiter machine:

```python
from vkbottle.bot import Bot, Message
from vkbottle.tools import WaiterMachine

bot = Bot("...")
wm = WaiterMachine()


@bot.on.message(text="/wm")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    # Следующая строчка остановит выполнение хендлера,
    # и исполнение пойдет дальше только когда будет получено
    # сообщение соответствующее заданным правилам
    # (в данном случае просто от того же пользователя)
    m, _ = await wm.wait(bot.on.message_view, message)
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


bot.run_forever()
```

Из `.wait` возвращается tuple с двумя элементами:

* Объект события которое разрешило ожидание (в примере выше, `Message`)
* Контекст который был сформирован в ходе обработки события

Поэтому его можно сразу раскрыть в две переменные.

В `.wait` можно так же передать правила, и `default_behaviour` как именованный аргумент.

```python
await message.answer("Напиши мне твой номер телефона")
m, ctx = await wm.wait(bot.on.message_view, message, RegexRule(PHONE_NUMBER_REGEX), default_behaviour="Неверный формат, напиши еще раз в правильном формате")
```

`default_behaviour` может принимать Callable, куда придет событие, либо любой другой объект который будет передан в return manager привязаный к активному view и обработан, в примере выше это строка, которая будет отправлена как сообщение, в соответствии с имплементацией в return manager для view сообщений ботов.
