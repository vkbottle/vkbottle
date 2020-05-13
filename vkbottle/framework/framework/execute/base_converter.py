import ast
import typing
from inspect import getsource
from vkbottle.utils import ContextInstanceMixin


class ConverterError(Exception):
    pass


class Area(ContextInstanceMixin):
    def __init__(self, **values):
        self.values = values
        self.set_current(self)


class Converter:
    """ Translate Python into the VKScript with AST """

    def __init__(self):
        self.definitions: typing.Dict[ast.AST, ast] = {}

    def __call__(self, for_definition: ast.AST):
        def decorator(func):
            self.definitions[for_definition] = func
            return func

        return decorator

    def find_definition(self, d):
        if d.__class__ not in self.definitions:
            raise ConverterError(f"Definition for {d.__class__} is undefined")
        return self.definitions[d.__class__](d)

    def scriptify(self, func: typing.Callable, **values) -> str:
        """ Translate function to VKScript """
        source = getsource(func)
        code = ast.parse(source).body[0]
        Area(**values)
        return "".join(self.find_definition(line) for line in code.body)
