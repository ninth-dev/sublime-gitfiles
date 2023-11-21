from enum import Enum
from typing import Self, Tuple

import sublime


class StatusUnknown:
    description: str

    def __init__(self, description):
        self.description = description


class StatusCode(Enum):
    ADDED = "A"
    UNMERGED = "U"
    DELETED = "D"
    MODIFIED = "M"
    RENAMED = "R"
    TYPE_CHANGED = "T"
    UNTRACKED = "?"
    IGNORED = "!"
    UNKNOWN = "X"

    def kind(self) -> Tuple[sublime.KindId, str, str]:
        return (self.__kindId(), str(self.value).lower(), self.__description())

    def __description(self) -> str:
        return {
            StatusCode.ADDED: "Added",
            StatusCode.UNMERGED: "Unmerged",
            StatusCode.DELETED: "Deleted",
            StatusCode.MODIFIED: "Modified",
            StatusCode.RENAMED: "Renamed",
            StatusCode.TYPE_CHANGED: "File Type Changed",
            StatusCode.UNTRACKED: "Untracked",
            StatusCode.IGNORED: "Ignored",
            StatusCode.UNKNOWN: "Unknown",
        }[self]

    def __kindId(self) -> sublime.KindId:
        return {
            StatusCode.ADDED: sublime.KIND_ID_COLOR_GREENISH,
            StatusCode.UNMERGED: sublime.KIND_ID_COLOR_REDISH,
            StatusCode.DELETED: sublime.KIND_ID_COLOR_REDISH,
            StatusCode.MODIFIED: sublime.KIND_ID_COLOR_ORANGISH,
            StatusCode.RENAMED: sublime.KIND_ID_COLOR_CYANISH,
            StatusCode.TYPE_CHANGED: sublime.KIND_ID_COLOR_CYANISH,
            StatusCode.UNTRACKED: sublime.KIND_ID_COLOR_BLUISH,
            StatusCode.IGNORED: sublime.KIND_ID_AMBIGUOUS,
            StatusCode.UNKNOWN: sublime.KIND_ID_AMBIGUOUS,
        }[self]


ValidStatusCode = StatusCode | StatusUnknown
