import sys

SUPPORTED_MODULES = ["json", "ujson", "hyperjson", "orjson"]
DOWNLOADED = [module for module in SUPPORTED_MODULES if module in sys.modules]
USAGE = DOWNLOADED[-1]

json = __import__(USAGE)
