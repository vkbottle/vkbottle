#!/usr/bin/env python

import sys

from setuptools import setup

sys.stderr.write(
    """
This installation method is just a workound for github dependency-graph
which doesn't support pyproject.toml metadata yet.
See: https://github.com/orgs/community/discussions/6456

Please use following command to install this package:
pip install .
"""
)
sys.exit(1)

setup(
    name="vkbottle",
    requires=[],
)
