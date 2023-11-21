from enum import Enum

import sublime


class GitStatusCode(Enum):
    ADDED = "A"
    DELETED = "D"
    MODIFIED = "M"
    RENAMED = "R"
    TYPE_CHANGED = "T"
    UNTRACKED = "??"
    IGNORED = "!!"

    # unmerged
    UNMERGED_BOTH_DELETED = "DD"
    UNMERGED_BOTH_MODIFIED = "UU"
    UNMERGED_BOTH_ADDED = "AA"
    UNMERGED_DELETED_BY_THEM = "DU"
    UNMERGED_ADDED_BY_THEM = "AU"
    UNMERGED_DELETED_BY_US = "UD"
    UNMERGED_ADDED_BY_US = "UA"

    UNKNOWN = "-"

    def kind_letter(self) -> str:
        return {
            GitStatusCode.ADDED: "a",
            GitStatusCode.DELETED: "d",
            GitStatusCode.MODIFIED: "m",
            GitStatusCode.RENAMED: "r",
            GitStatusCode.TYPE_CHANGED: "t",
            GitStatusCode.UNTRACKED: "?",
            GitStatusCode.IGNORED: "!",
            GitStatusCode.UNMERGED_BOTH_DELETED: "u",
            GitStatusCode.UNMERGED_BOTH_MODIFIED: "u",
            GitStatusCode.UNMERGED_BOTH_ADDED: "u",
            GitStatusCode.UNMERGED_DELETED_BY_THEM: "u",
            GitStatusCode.UNMERGED_ADDED_BY_THEM: "u",
            GitStatusCode.UNMERGED_DELETED_BY_US: "u",
            GitStatusCode.UNMERGED_ADDED_BY_US: "u",
            GitStatusCode.UNKNOWN: "-",
        }[self]

    def description(self) -> str:
        return {
            GitStatusCode.ADDED: "Added",
            GitStatusCode.DELETED: "Deleted",
            GitStatusCode.MODIFIED: "Modified",
            GitStatusCode.RENAMED: "Renamed",
            GitStatusCode.TYPE_CHANGED: "File Type Changed",
            GitStatusCode.UNTRACKED: "Untracked",
            GitStatusCode.IGNORED: "Ignored",
            GitStatusCode.UNMERGED_BOTH_DELETED: "Unmerged, both deleted",
            GitStatusCode.UNMERGED_BOTH_MODIFIED: "Unmerged, both modified",
            GitStatusCode.UNMERGED_BOTH_ADDED: "Unmerged, both added",
            GitStatusCode.UNMERGED_DELETED_BY_THEM: "Unmerged, deleted by them",
            GitStatusCode.UNMERGED_ADDED_BY_THEM: "Unmerged, added by them",
            GitStatusCode.UNMERGED_DELETED_BY_US: "Unmerged, deleted by us",
            GitStatusCode.UNMERGED_ADDED_BY_US: "Unmerged, added by us",
            GitStatusCode.UNKNOWN: "Unknown",
        }[self]

    def kind_id(self) -> sublime.KindId:
        return {
            GitStatusCode.ADDED: sublime.KIND_ID_COLOR_GREENISH,
            GitStatusCode.DELETED: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.MODIFIED: sublime.KIND_ID_COLOR_ORANGISH,
            GitStatusCode.RENAMED: sublime.KIND_ID_COLOR_CYANISH,
            GitStatusCode.TYPE_CHANGED: sublime.KIND_ID_COLOR_CYANISH,
            GitStatusCode.UNTRACKED: sublime.KIND_ID_COLOR_BLUISH,
            GitStatusCode.IGNORED: sublime.KIND_ID_AMBIGUOUS,
            GitStatusCode.UNMERGED_BOTH_DELETED: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_BOTH_MODIFIED: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_BOTH_ADDED: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_DELETED_BY_THEM: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_ADDED_BY_THEM: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_DELETED_BY_US: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNMERGED_ADDED_BY_US: sublime.KIND_ID_COLOR_REDISH,
            GitStatusCode.UNKNOWN: sublime.KIND_ID_AMBIGUOUS,
        }[self]
