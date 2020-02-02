from collections import MutableMapping
from typing import Sequence
import os


def dict_of_dicts_merge(d1, d2):
    """
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    """
    for k, v in d1.items():
        if k in d2:
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = dict_of_dicts_merge(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def except_none_self(adict: dict) -> dict:
    ndict = {}
    for k, v in adict.items():
        if (
                k not in ["self", "cls"]
                and v is not None and not k.startswith("__")
        ):
            ndict.update({k: v})
    return ndict


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


def folder_checkup(path, create: bool = True):
    path = os.path.abspath(path)
    if not os.path.exists(path) and create:
        os.mkdir(path)
    return path
