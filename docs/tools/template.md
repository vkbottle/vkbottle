# Template

Посмотреть как применять темплейты можно [здесь](https://vk.com/dev/bot_docs_templates)

Для создания темплейтов есть `template_gen`

Импортируйте нужные компоненты:

```python
from vkbottle import TemplateElement, template_gen

my_template = template_gen(
    TemplateElement(...), # о том как нужно сочетать параметры можно
    TemplateElement(...)  # прочитать в документации вконтакте выше
)

# my_template - готовый для отправки json
# ...
await message.answer("Держи карусель!", template=my_template)
```
