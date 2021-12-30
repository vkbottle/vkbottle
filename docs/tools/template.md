# Template

Посмотреть как применять темплейты можно [здесь](https://dev.vk.com/api/bots/development/messages#Шаблоны%20сообщений)

Для создания темплейтов есть `template_gen`

Импортируйте нужные компоненты:

```python
from vkbottle import TemplateElement, template_gen

my_template = template_gen(
    TemplateElement(...), # о том как нужно сочетать параметры можно
    TemplateElement(...)  # прочитать в документации Вконтакте выше
)

# my_template - готовый для отправки json
# ...
await message.answer("Держи карусель!", template=my_template)
```
