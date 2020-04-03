import requests
import typing
import json
import os


def to_shake_case(text: str):
    return "".join(
        [letter if letter.islower() else "_" + letter.lower() for letter in text]
    )


SCHEMA_URL = "https://raw.githubusercontent.com/VKCOM/vk-api-schema/master/methods.json"
SCHEMA = json.loads(requests.get(SCHEMA_URL).text)
SIGNATURE = "Generated with love"
WRAPPING = "\n        "
PATH = "../"
TYPES = {
    "integer": "int",
    "string": "str",
    "array": "typing.List",
    "object": "dict",
    "boolean": "bool",
}


# Split method classes and method names
filtered: typing.Dict[str, dict] = {}
for pattern in SCHEMA["methods"]:
    method = pattern["name"].split(".")
    if method[0] not in filtered:
        filtered[method[0]] = {}
    filtered[method[0]].update({method[1]: pattern})


m_classes = []
for method_class, methods in filtered.items():
    response_model_exists = os.path.exists(
        f"/Users/arsenijkruckov/vkbottle/vkbottle/types/responses/{method_class}.py"
    )
    print(method_class, response_model_exists)
    filename = PATH + to_shake_case(method_class) + ".py"
    with open(filename, "w") as file:
        file.writelines(
            f"""# {SIGNATURE}
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod""".splitlines(
                keepends=True
            )
        )
        lines = []
        class_names = []
        for name, method in methods.items():
            docstring = f'''
        """ {method_class}.{name}
        From Vk Docs: {method.get("description", "")}
        Access from {", ".join(method["access_token_type"])} token(s)
        {WRAPPING.join([f":param {p['name']}: {p.get('description', '')}" for p in method.get("parameters", ())])}
        """\n'''
            params = [
                f"{p['name'] if p['name'] not in ['global'] else p['name'] + '_'}: {TYPES.get(p['type'], 'typing.Any') if 'type' in p else 'typing.Any'}"
                + (" = None" if not p.get("required") else "")
                for p in method.get("parameters", ())
            ]
            params = params
            newparams = []
            for i, p in enumerate(params):
                if " = None" not in p:
                    newparams.append(params.pop(i))
            newparams += params
            if method_class == "groups":
                print(params)
                print(newparams)
            params = ", ".join(newparams)

            class_name = method_class.capitalize() + (
                name.capitalize() if name.islower() else name[0].upper() + name[1:]
            )
            class_names.append((name, class_name))
            code = (
                """
        params = {k if not k.endswith("_") else k[:-1]: v for k, v in locals().items() if k not in ["self"] and v is not None}
        return await self.request("""
                + f'"{method_class}.{name}", params'
                + (
                    f", response_model=responses.{to_shake_case(method_class)}.{name[0].upper() + name[1:]}"
                    if response_model_exists
                    else ""
                )
                + """)"""
            )
            lines.extend(
                [
                    f"\n\n\nclass {class_name}(BaseMethod):",
                    f"\n    access_token_type: APIAccessibility = [{', '.join([f'APIAccessibility.{a.upper()}' for a in method.get('access_token_type', [])])}]\n",
                    f"\n    async def __call__(self, {params})"
                    + (
                        f" -> responses.{to_shake_case(method_class)}.{name[0].upper() + name[1:]}:"
                        if response_model_exists
                        else ":"
                    ),
                    *docstring.splitlines(keepends=True),
                    code,
                ]
            )
        file.writelines(lines)
        file.writelines(
            [
                "\n\n",
                f"\nclass {method_class.capitalize()}:",
                "\n    def __init__(self, request):",
                *[
                    f"\n        self.{to_shake_case(n)} = {mc}(request)"
                    for n, mc in class_names
                ],
                "\n",
            ]
        )
        m_classes.append(method_class)

"""
with open(PATH + "__init__.py", "w") as init:
    init.writelines(
        [
            f"from .{to_shake_case(method_class)} import {method_class.capitalize()}\n"
            for method_class in m_classes
        ]
        + [f"\n__all__ = [{', '.join([c.capitalize() for c in m_classes])}]\n"]
    )
"""
