import pkg_resources

SUPPORTED_MODULES = ["json", "ujson", "hyperjson", "orjson"]
DOWNLOADED = [pkg.key for pkg in pkg_resources.working_set if pkg.key in SUPPORTED_MODULES]
USAGE = DOWNLOADED[-1]

json = __import__(USAGE)
