from .abc import ABCResponseValidator
from .json_validator import JSONValidator
from .vk_api_error_validator import VKAPIErrorValidator

DEFAULT_RESPONSE_VALIDATORS = [
    JSONValidator(),
    VKAPIErrorValidator(),
]
