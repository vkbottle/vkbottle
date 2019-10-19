from ...api.exceptions import BranchError
from ...utils import folder_checkup
import re
import logging


BRANCH_DATA = '.BRANCHES.txt'


class BranchManager:
    def __init__(self, plugin_folder: str):
        self.plugin_folder = folder_checkup(plugin_folder)
        self.log_path = '{path}/{br_file}'.format(path=self.plugin_folder,
                                                  br_file=BRANCH_DATA)
        self._meet_up = dict()
        self._branch_queue = dict()

    def simple_branch(self, branch_name: str):
        def decorator(func):
            self._meet_up[branch_name] = func
            return func
        return decorator

    @property
    def queue(self):
        return self._branch_queue

    @property
    def branches(self):
        return self._meet_up

    def add(self, uid: int, branch: str) -> None:
        if branch not in self._meet_up:
            raise BranchError('Branch "{}" is undefined'.format(branch))
        self._branch_queue[uid] = branch

    def load(self, uid: int) -> str:
        if uid in self._branch_queue:
            return self._branch_queue.get(uid, None)

    def exit(self, uid: int):
        if uid in self._branch_queue:
            return self._branch_queue.pop(uid, None)
