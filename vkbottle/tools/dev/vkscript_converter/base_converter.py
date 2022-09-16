import ast
from inspect import getsource
from typing import Callable, Dict, Type


class ConverterError(Exception):
    pass


class Converter:
    """Translate Python into the VKScript with AST"""

    def __init__(self):
        self.definitions: Dict[Type[ast.AST], Callable] = {}

    def __call__(self, for_definition: Type[ast.AST]):
        def decorator(func):
            self.definitions[for_definition] = func
            return func

        return decorator

    def find_definition(self, d):
        if d.__class__ not in self.definitions:
            raise ConverterError(
                f"Definition for {d.__class__} is undefined. Maybe vkscript doesn't support it"
            )
        return self.definitions[d.__class__](d)

    def scriptify(self, func: Callable, *args_values, **kwargs_values) -> str:
        """Translate function to VKScript"""
        source = getsource(func)
        code: ast.FunctionDef = ast.parse(source).body[0]  # type: ignore
        # Check if function has *args or **kwargs
        if code.args.vararg or code.args.kwarg:
            raise ConverterError("VKScript converter doesn't support *args and **kwargs")
        # Get list of function arguments names
        args = [a.arg for a in code.args.args]
        # Get list of function arguments default values
        defaults = [self.find_definition(d) for d in code.args.defaults]
        # Check that first argument is api
        if not args or args[0] != "api":
            raise ConverterError("First argument must be api")
        # Remove api from args
        args = args[1:]
        # Cycle through function arguments and check if they values are passed
        for arg, v in zip(args, args_values):
            if arg in kwargs_values:
                continue
            kwargs_values[arg] = v
        # Default values are used if values are not passed
        # eg func(a, b=2, c=3) -> func(1, 3), args = [a=1, b=3, c=3], defaults = [2, 3]
        for arg in args[::-1]:
            if not defaults and arg not in kwargs_values:
                raise ConverterError(f"Argument {arg} is not provided")
            if arg in kwargs_values:
                continue
            kwargs_values[arg] = defaults.pop()
        # Create assignments for every argument as variable
        values_assignments = [f"var {k}={v};" for k, v in kwargs_values.items()]
        return "".join(values_assignments) + "".join(
            self.find_definition(line) for line in code.body
        )
