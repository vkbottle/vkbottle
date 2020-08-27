from .abc import ABCResponseValidator
from .json_validator import JSONValidator
from .vk_api_error_validator import VKAPIErrorValidator
from .get_response_validator import GetResponseValidator

DEFAULT_RESPONSE_VALIDATORS = [
    JSONValidator(),
    VKAPIErrorValidator(),
    GetResponseValidator(),
]
