# Token-Generator

У VK существуют лимиты на запросы, но эти лимиты легко обходятся при наличии нескольких токенов, для того чтобы автоматически распределять токены на каждый запрос используются токен генераторы, существуют 2 вида генераторов из коробки:

* `SingleTokenGenerator` - используется один токен на все запросы, принимает строку

* `ConsistentTokenGenerator` - используется несколько токенов поочередно, если вы хотите его использовать грамотно, необходимо рассчитать нагрузку по времени, лимит вконтакте на запросы для ботов - 25/сек, для пользователей - 3/сек, принимает лист из строк

По правилам vkbottle вы конечно же можете реализовать свой генератор, базируясь на интерфейсе [ABCTokenGenerator](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/api/token_generator/abc.py)
