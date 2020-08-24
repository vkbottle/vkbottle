from choicelib import choice_in_order

json = choice_in_order(["ujson", "hyperjson", "orjson"], do_import=True, default="json")
logger = choice_in_order(["loguru"], do_import=True, default="logging")
