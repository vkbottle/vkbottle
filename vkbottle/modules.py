from choicelib import choice_in_order

json = choice_in_order(["json", "ujson", "hyperjson", "orjson"], do_import=True)
logger = choice_in_order(["logging", "loguru"], do_import=True)
