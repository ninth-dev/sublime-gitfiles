from typing import NamedTuple, Optional, Tuple

import sublime

from .status_code import StatusCode, UnmergedStatusCode, ValidStatusCode


class GitFileStatus(NamedTuple):
    index_status: str
    working_tree_status: str

    def __safe_status_code(
        self, code: str, default: ValidStatusCode
    ) -> ValidStatusCode:
        try:
            return StatusCode(code)
        except:
            return default

    def __safe_unmerged_status_code(self, code: str) -> Optional[ValidStatusCode]:
        try:
            return UnmergedStatusCode(code)
        except:
            return None

    def kind(self) -> Tuple[sublime.KindId, str, str]:
        status_code = self.code()
        return (
            status_code.kind_id(),
            status_code.kind_letter(),
            f"{status_code.description()} [{self.index_status}{self.working_tree_status}]",
        )

    def code(self) -> ValidStatusCode:
        index_status = self.index_status
        working_tree_status = self.working_tree_status
        both_status = f"{index_status}{working_tree_status}"

        # unmerged
        status_code = self.__safe_unmerged_status_code(both_status)

        if status_code is not None:
            return status_code

        if index_status == " " and not working_tree_status == " ":
            # not staged
            return self.__safe_status_code(working_tree_status, StatusCode.UNKNOWN)

        if working_tree_status == " " and not index_status == " ":
            # staged
            return self.__safe_status_code(working_tree_status, StatusCode.UNKNOWN)

        # if (index_status == "?" and working_tree_status == "?") or (
        #     index_status == "!" and working_tree_status == "!"
        # ):
        status_code = self.__safe_status_code(both_status, StatusCode.UNKNOWN)

        # otherwise use working_tree_status
        if status_code is StatusCode.UNKNOWN:
            return self.__safe_status_code(working_tree_status, status_code)
        else:
            return status_code


class GitFile(NamedTuple):
    file_name: str
    file_path: str
    git_status: GitFileStatus
