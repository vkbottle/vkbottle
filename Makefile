# Treat these arguments not as files, but as recipes
.PHONY: help minimal init check fix publish

# Used to execute all in one shell
.ONESHELL:

# Default recipe
.DEFAULT: help
help:
	@echo "make minimal"
	@echo "	   install minimal dependencies"
	@echo "make init"
	@echo "	   install all dependencies and dev hooks"
	@echo "make check"
	@echo "	   run tests and linters"
	@echo "make fix"
	@echo "	   fix code with black and autoflake"
	@echo "make publish"
	@echo "	   publish to PyPi using PYPI_TOKEN"

# Define canned (reusable) recipe for installing poetry and virtualenv
define install =
	@echo;
	@echo "Installing poetry"
	@echo "=================";
	@pip install poetry
	@echo;
	@echo "Installing virtualenv"
	@echo "=====================";
	@pip install virtualenv --use-feature=2020-resolver
endef

minimal:
	$(install)
	@echo;
	@echo "Installing dependencies"
	@echo "=======================";
	@poetry install --no-dev

init:
	$(install)
	@echo;
	@echo "Installing dependencies"
	@echo "=======================";
	@poetry install
	@echo;
	@echo "Installing pre-commit and pre-push hooks"
	@echo "========================================";
	@pre-commit install -t=pre-commit -t=pre-push

check:
	@poetry run mypy vkbottle
	@poetry run flake8
	@poetry run pytest --cov vkbottle tests

fix:
	@black .
	@autoflake --recursive --in-place --exclude=__init__.py,bot.py,venv --remove-all-unused-imports --remove-duplicate-keys .

publish:
	poetry build
	poetry config pypi-token.pypi ${PYPI_TOKEN}
	poetry publish; true # "; true" is used to ignore command exit code so that rm -rf can execute anyway
	rm -rf dist/
