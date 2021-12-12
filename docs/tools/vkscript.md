# Vkscript Converter

Просто импортируйте `vkscript` из библиотеки и напишите функцию, которая будет работать с api для того, обернув в декоратор, чтобы после ее вызова вам вернулся код выполняющий логику вашей функции, но в `VKScript`

```python
from vkbottle import vkscript

@vkscript
def my_execute(api, user_ids=()):
    message_ids = []
    for user_id in user_ids:
        user = api.users.get(user_ids=user_id)[0]
        message_ids.append(api.messages.send(message=f"{user.first_name}, спасибо что зашел на чай", random_id=0, peer_id=user_id))
    return message_ids

# далее вызывая эту функцию вы можете использовать ее ответ в качестве кода для execute

await api.execute(code=my_execute(user_ids=[10, 11, 12]))
```
