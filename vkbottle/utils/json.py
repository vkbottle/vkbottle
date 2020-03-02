import pkg_resources

SUPPORTED_MODULES = ["ujson", "hyperjson", "orjson"]
DOWNLOADED = [
    pkg.key for pkg in pkg_resources.working_set if pkg.key in SUPPORTED_MODULES
]
USAGE = DOWNLOADED[-1] if DOWNLOADED else "json"

json = __import__(USAGE)
