# Template
## Carousel
Import elements:
```python
from vkbottle import template_gen, TemplateElement
```
`template_gen` - create template json by the template elements

Example:
```python
from vkbottle import template_gen, TemplateElement, keyboard_gen

template = template_gen(
    TemplateElement(
        "A title",
        "A description",
        "-189607270_457240272",
        buttons=keyboard_gen(
            [[
                {"label": "A button"}, 
                {"type": "open_link", "link": "https://google.com", "label": "A link"}
            ]]
        )
    ),
    TemplateElement(
        "A title of second element",
        "Second element description",
        "-189607270_457240272",
        buttons=keyboard_gen(
            [[
                {"label": "A button"},
                {"type": "open_link", "link": "https://github.com/timoniq/vkbottle", "label": "An another link"}
            ]]
        )
    )
)
```
To send a carousel:
```python
# I your message handler
await ans("Hurray!", template=template)
```