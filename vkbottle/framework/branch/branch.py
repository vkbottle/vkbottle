from ...api.exceptions import BranchError
from ...utils import folder_checkup
import typing

BRANCH_DATA = ".BRANCHES.txt"


class BranchManager:
    def __init__(self, plugin_folder: str):
        self.plugin_folder: str = folder_checkup(plugin_folder)
        self.log_path: str = "{path}/{branch_file}".format(
            path=self.plugin_folder, branch_file=BRANCH_DATA
        )
        self._meet_up: dict = {}
        self._branch_queue: dict = {}

    def simple_branch(self, branch_name: str):
        def decorator(func):
            self._meet_up[branch_name] = func
            return func

        return decorator

    @property
    def queue(self) -> dict:
        return self._branch_queue

    @property
    def branches(self) -> dict:
        return self._meet_up

    def add(self, uid: int, branch: str, **kwargs) -> None:
        if branch not in self._meet_up:
            raise BranchError('Branch "{}" is undefined'.format(branch))
        self._branch_queue[uid] = [branch, kwargs]

    def load(self, uid: int) -> typing.Optional[typing.List]:
        if uid in self._branch_queue:
            return self._branch_queue.get(uid, None)

    def exit(self, uid: int) -> typing.Optional[typing.List]:
        if uid in self._branch_queue:
            return self._branch_queue.pop(uid, None)
