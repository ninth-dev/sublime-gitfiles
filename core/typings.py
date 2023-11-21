from typing import NamedTuple, Tuple
from .status_code import StatusCode

class GitFileStatus(NamedTuple):
    index_status: str
    working_tree_status: str

    def __status_description(self, code: str) -> StatusCode
        try:
            return StatusCode(code)
        except:
            return StatusCode.UNKNOWN

    def details(self) -> Tuple[str, str]:
        index_status = self.index_status
        working_tree_status = self.working_tree_status

        if index_status == "?" and working_tree_status == "?":
            return ("?", "Untracked")

        if index_status == "!" and working_tree_status == "!":
            return ("!", "Ignored")

        if index_status == " " and not working_tree_status == " ":
            # not staged
            return self.__status_description(working_tree_status)

        if working_tree_status == " " and not index_status == " ":
            # staged
            (code, description) = self.__status_description(index_status)
            return (code, f"{description}*")

        # ---- unmerged
        if working_tree_status == index_status and working_tree_status == "D":
            return ("u", "Unmerged, both deleted")
        if working_tree_status == index_status and working_tree_status == "U":
            return ("u", "Unmerged, both modified")
        if working_tree_status == index_status and working_tree_status == "A":
            return ("u", "Unmerged, both added")
        if working_tree_status == "U" and index_status == "D":
            return ("u", "Unmerged, deleted by them")
        if working_tree_status == "U" and index_status == "A":
            return ("u", "Unmerged, added by them")
        if index_status == "U" and working_tree_status == "D":
            return ("u", "Unmerged, deleted by us")
        if index_status == "U" and working_tree_status == "D":
            return ("u", "Unmerged, added by us")
        # ---- unmerged ends

        # working_tree_status takes precedence for description
        # append [XY]
        (code, description) = self.__status_description(working_tree_status)
        return (code, f"{description} [{index_status}{working_tree_status}]")


class GitFile(NamedTuple):
    file_name: str
    file_path: str
    git_status: GitFileStatus
