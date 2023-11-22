from typing import Tuple

import sublime

from .git_status_code import GitStatusCode


class GitStatus:
    status_code: GitStatusCode
    index_status: str
    working_tree_status: str

    def __init__(self, index_status: str, working_tree_status: str):
        self.index_status = index_status
        self.working_tree_status = working_tree_status
        # first look for single status, unmerged status, ignored and untracked
        # if no match use working tree status only
        self.status_code = self.__safe_status_code(
            f"{index_status}{working_tree_status}".strip(),
            self.__safe_status_code(working_tree_status, GitStatusCode.UNKNOWN),
        )

    def __safe_status_code(self, code: str, default: GitStatusCode) -> GitStatusCode:
        try:
            return GitStatusCode(code)
        except:
            return default

    def kind(self) -> Tuple[sublime.KindId, str, str]:
        return (
            self.status_code.kind_id(),
            self.status_code.kind_letter(),
            "",
        )

    def description(self) -> str:
        return f"{self.status_code.description()} [{self.index_status}{self.working_tree_status}]"
