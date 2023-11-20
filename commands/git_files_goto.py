import re
from functools import partial
from pathlib import Path

import sublime
import sublime_plugin

from ..core.git import git_status_porcelain
from ..core.parser import parse_git_status
from ..core.typings import (
    KIND_ADDED,
    KIND_CONFLICTED,
    KIND_DELETED,
    KIND_MODIFIED,
    KIND_RENAMED,
    KIND_TYPE_CHANGED,
    KIND_UNTRACKED,
)

GIT_STATUS_KIND_MAPPING = {
    "a": KIND_ADDED,
    "c": KIND_CONFLICTED,
    "d": KIND_DELETED,
    "m": KIND_MODIFIED,
    "r": KIND_RENAMED,
    "t": KIND_TYPE_CHANGED,
    "?": KIND_UNTRACKED,
}


class GitFilesGotoCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = Path(self.window.extract_variables()["folder"])
        output = git_status_porcelain(cwd)
        git_files = parse_git_status(output)
        # print(git_files)

        if len(git_files) > 0:
            self.window.show_quick_panel(
                items=self.to_quick_panel_item(git_files),
                on_select=partial(self.on_select, cwd, git_files),
                on_highlight=partial(self.on_highlight, cwd, git_files),
            )
        else:
            sublime.message_dialog("GitFiles: No changed files.")

    def to_quick_panel_item(self, git_files):
        items = []
        for item in git_files:
            # print(item.file_name)
            git_status_details = item.git_status.details()
            (annotation, git_status_description) = git_status_details
            items.append(
                sublime.QuickPanelItem(
                    item.file_name,
                    item.file_path,
                    git_status_description,
                    GIT_STATUS_KIND_MAPPING.get(
                        annotation,
                        (sublime.KIND_ID_AMBIGUOUS, annotation, ""),
                    ),
                )
            )
        return items

    def __open_file(self, cwd, items, index: int, on_highlight: bool):
        if index > -1:
            rename_match = re.search(r"(.+) -> (.*)", items[index].file_path)
            file_path = (
                rename_match.group(2)
                if rename_match is not None
                else items[index].file_path
            )
            full_path = Path(cwd, file_path)
            new_file_flag = (
                sublime.NewFileFlags.TRANSIENT
                if on_highlight
                else sublime.NewFileFlags.NONE
            )
            if full_path.is_file():
                self.window.open_file(str(full_path), new_file_flag)

    def on_select(self, cwd, items, index: int):
        self.__open_file(cwd, items, index, False)

    def on_highlight(self, cwd, items, index: int):
        self.__open_file(cwd, items, index, True)
