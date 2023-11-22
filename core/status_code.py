from enum import Enum
from typing import Union

import sublime


class StatusCode(Enum):
    ADDED = "A"
    DELETED = "D"
    MODIFIED = "M"
    RENAMED = "R"
    TYPE_CHANGED = "T"
    UNTRACKED = "??"
    IGNORED = "!!"

    UNKNOWN = "X"

    def kind_letter(self) -> str:
        return {
            StatusCode.ADDED: "a",
            StatusCode.DELETED: "d",
            StatusCode.MODIFIED: "m",
            StatusCode.RENAMED: "r",
            StatusCode.TYPE_CHANGED: "t",
            StatusCode.UNTRACKED: "?",
            StatusCode.IGNORED: "!",
            StatusCode.UNKNOWN: "-",
        }[self]

    def description(self) -> str:
        return {
            StatusCode.ADDED: "Added",
            StatusCode.DELETED: "Deleted",
            StatusCode.MODIFIED: "Modified",
            StatusCode.RENAMED: "Renamed",
            StatusCode.TYPE_CHANGED: "File Type Changed",
            StatusCode.UNTRACKED: "Untracked",
            StatusCode.IGNORED: "Ignored",
            StatusCode.UNKNOWN: "Unknown",
        }[self]

    def kind_id(self) -> sublime.KindId:
        return {
            StatusCode.ADDED: sublime.KIND_ID_COLOR_GREENISH,
            StatusCode.DELETED: sublime.KIND_ID_COLOR_REDISH,
            StatusCode.MODIFIED: sublime.KIND_ID_COLOR_ORANGISH,
            StatusCode.RENAMED: sublime.KIND_ID_COLOR_CYANISH,
            StatusCode.TYPE_CHANGED: sublime.KIND_ID_COLOR_CYANISH,
            StatusCode.UNTRACKED: sublime.KIND_ID_COLOR_BLUISH,
            StatusCode.IGNORED: sublime.KIND_ID_AMBIGUOUS,
            StatusCode.UNKNOWN: sublime.KIND_ID_AMBIGUOUS,
        }[self]


class UnmergedStatusCode(Enum):
    UNMERGED_BOTH_DELETED = "DD"
    UNMERGED_BOTH_MODIFIED = "UU"
    UNMERGED_BOTH_ADDED = "AA"
    UNMERGED_DELETED_BY_THEM = "DU"
    UNMERGED_ADDED_BY_THEM = "AU"
    UNMERGED_DELETED_BY_US = "UD"
    UNMERGED_ADDED_BY_US = "UA"

    def kind_letter(self) -> str:
        return "u"

    def description(self) -> str:
        return {
            UnmergedStatusCode.UNMERGED_BOTH_DELETED: "Unmerged, both deleted",
            UnmergedStatusCode.UNMERGED_BOTH_MODIFIED: "Unmerged, both modified",
            UnmergedStatusCode.UNMERGED_BOTH_ADDED: "Unmerged, both added",
            UnmergedStatusCode.UNMERGED_DELETED_BY_THEM: "Unmerged, deleted by them",
            UnmergedStatusCode.UNMERGED_ADDED_BY_THEM: "Unmerged, added by them",
            UnmergedStatusCode.UNMERGED_DELETED_BY_US: "Unmerged, deleted by us",
            UnmergedStatusCode.UNMERGED_ADDED_BY_US: "Unmerged, added by us",
        }[self]

    def kind_id(self) -> sublime.KindId:
        return {
            UnmergedStatusCode.UNMERGED_BOTH_DELETED: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_BOTH_MODIFIED: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_BOTH_ADDED: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_DELETED_BY_THEM: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_ADDED_BY_THEM: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_DELETED_BY_US: sublime.KIND_ID_COLOR_REDISH,
            UnmergedStatusCode.UNMERGED_ADDED_BY_US: sublime.KIND_ID_COLOR_REDISH,
        }[self]


ValidStatusCode = Union[StatusCode, UnmergedStatusCode]
