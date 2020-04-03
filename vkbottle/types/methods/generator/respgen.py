import requests
import typing
import json
import os


def to_shake_case(text: str):
    return "".join(
        [letter if letter.islower() else "_" + letter.lower() for letter in text]
    )


def first_big_letter(text: str):
    return text[0].upper() + text[1:]


SCHEMA_URL = (
    "https://raw.githubusercontent.com/VKCOM/vk-api-schema/master/responses.json"
)
SCHEMA_OBJECTS_URL = (
    "https://raw.githubusercontent.com/VKCOM/vk-api-schema/master/objects.json"
)
SCHEMA = json.loads(requests.get(SCHEMA_URL).text)
SCHEMA_OBJECTS = json.loads(requests.get(SCHEMA_OBJECTS_URL).text)
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
for pattern in SCHEMA["definitions"]:
    f = pattern.split("_")
    class_name = f[0]
    method = f[1:-1]

    print(f"{class_name}.{method}")

print(filtered)
