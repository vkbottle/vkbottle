# Рекомендации

Установка окружения через `python-poetry` (`poetry install`)

Для автоматического форматинга и линтинга лучше использовать `pre-commit` и `pre-push` хуки. Включить их можно через `poetry run pre-commit install -t=pre-commit -t=pre-push`

> ⚠️ Мы используем `flakeheaven` вместо `flake8`, так как он позволяет более гибко настраивать плагины.
