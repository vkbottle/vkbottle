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


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


def folder_checkup(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.mkdir(path)
    return path
