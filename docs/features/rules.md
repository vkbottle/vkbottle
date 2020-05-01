
Правила обработки сообщений по стандарту обрабатываются с помощью правила VBMLRule (`vkbottle.rule.VBMLRule`), но что если в задачу хендлера входит прием например сообщений с каким-то вложением. Для начала давайте разберемся как работают правила:  
```python
from vkbottle.rule import ChatActionRule
# Импортировали стандартное правило на событие в чате

@bot.on.message(ChatActionRule("chat_invite_user", "chat_invite_user_by_link"))
async def wrapper(ans: Message):
    await ans(f'Ура! Новый участник в нашей беседе')
```

### Стандартные правила: 

  - `AttachmentRule(attachment_type)`
  - `ChatActionRule(chat_action_type, required)`
  - `VBMLRule(pattern/str/list[pattern/str])`
  - `PayloadRule(payload as dict)`
  - `EventRule(events)`

Для создания собственных правил могут понадобиться абстрактные классы: `AbstractRule`, `AbstractMessageRule` 

```python
from vkbottle.rule import AbstractMessageRule

# Создаем класс для правила
class OnlyMe(AbstractMessageRule):
    async def check(self, message: Message):
        # Функция check вызывается при проверке правила
        if message.from_id == 1: # Если пользователь, написавший сообщение имеет id = 1
            return True # Проверка пройдена

@bot.on.message(OnlyMe(), text="/admincommand")
async def wrapper(ans: Message):
    await ans("Команда доступна только одному человеку :)")
```