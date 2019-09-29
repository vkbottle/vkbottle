"""Read LICENSE.txt"""

from ...utils import Logger
from .whitelist import WhiteList
from .validators import RegexValidators
from inspect import getmembers, ismethod
from typing import Optional, ClassVar


class Patcher(WhiteList):
    """VKBottle Patcher version 0.1
    Needed for:
    * Validators Support
    * WhiteList Support
    """
    def __init__(self, logger: Logger, plugin_folder: str):
        self.logger: Logger = logger
        self.use_whitelist: bool = False
        self.plugin_folder: str = plugin_folder
        self.regex_validators: dict = self.__provide_validators(RegexValidators)
        self.disable_validators: bool = False

        self.whitelist: list = list()

    def __call__(self, validators: ClassVar = None, disable_validators: bool = None, **validators_kwargs):
        if validators:
            self.regex_validators = self.__provide_validators(validators, validators_kwargs)
        if disable_validators:
            self.disable_validators = True

    @staticmethod
    def __provide_validators(validators, validators_kwargs: dict = None) -> dict:
        members_tuple = getmembers(validators(**validators_kwargs if validators_kwargs else {}), predicate=ismethod)
        return dict((x, y) for x, y in members_tuple if not x.startswith('__'))

    async def check_validators(self, check_object: dict, keys: dict):
        if not self.disable_validators:

            validators = check_object['validators']
            valid_dict: Optional[dict] = {}

            for key in keys:
                if key in validators:
                    for validator in validators[key]:
                        k = await self.regex_validators[validator](keys[key])
                        if k is None:
                            valid_dict = None
                            break
                        else:
                            valid_dict[key] = k
                else:
                    valid_dict = keys

            return valid_dict

        return keys

    def get_current(self) -> dict:
        return {
            'plugin_folder': self.plugin_folder,
            'use_whitelist': self.use_whitelist
            }

    def __repr__(self):
        return '<Patcher plugin_folder=\'{}\' use_whitelist={}>'.format(*self.get_current().values())
