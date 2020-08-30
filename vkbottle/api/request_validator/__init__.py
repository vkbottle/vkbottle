from .abc import ABCRequestValidator
from .translate_friendly_types_validator import TranslateFriendlyTypesValidator

DEFAULT_REQUEST_VALIDATORS = [TranslateFriendlyTypesValidator()]
