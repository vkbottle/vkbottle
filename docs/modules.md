# Dependencies customisation

VKBottle автоматически выбирает лучшую альтернативу для стандартных библиотек.

Эти библиотеки не указаны в зависимостях, поэтому вы должны установить их сами.

## JSON

В порядке убывания: `orjson`, `hyperjson`, `ujson`, `json`

## Logging

В порядке убывания: `loguru`, `logging`

!!! warning "Внимание"
    Мы настоятельно рекомендуем использовать `loguru` вместо `logging`. Возможно, он станет обязательной зависимостью в будущих релизах.

!!! info "Примечание"

    По умолчанию уровень логирования выставлен на `DEBUG`.
Изменить это вы можете так:

### Для logging

```python
import logging
logging.getLogger("vkbottle").setLevel(logging.INFO)
```

### Для loguru

Отключить логирование полностью

```python
from loguru import logger
logger.disable("vkbottle")
```

Установить определенный уровень

```python
import sys
from loguru import logger
logger.remove()
logger.add(sys.stderr, level="INFO")
```

Или установить [переменную окружения](https://en.wikipedia.org/wiki/Environment_variable) `LOGURU_LEVEL`
