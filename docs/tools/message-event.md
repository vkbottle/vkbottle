# MessageEvent

Обработка `callback` кнопок выходит на новый уровень:

```python
from vkbottle import GroupEventType
from vkbottle.bot import MessageEvent

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def handle_message_event(event: MessageEvent):
    await event.show_snackbar("Сейчас я исчезну")
```

* Никакого `object`. Всё находится уже в `event`, вместе с `group_id`
* Поддержка всех генераторов `event-data` при помощи соответствующими функциями
* Поддержка рулзов, связанных с `payload`
* Так же есть `message_edit` и `message_send`
