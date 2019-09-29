"""Read LICENSE.txt"""

"""
JSON TO UJSON - Switcher
"""

json_module = 'json'

try:
    import ujson as json
    json_module = 'ujson'
except ImportError:
    import json


def json_type_utils():
    if json_module == 'ujson':
        return 'You are using \x1b[35mFAST\x1b[0m JSON-Compiler based on UJSON'
    return 'You are using \x1b[35mSTANDART\x1b[0m JSON-Compiler. Download UJSON module to make it fast'


def dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs)
