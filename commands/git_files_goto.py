from functools import partial
from pathlib import Path

import sublime
import sublime_plugin

from ..common.git import GIT_STATUS_KIND_MAPPING, get_git_files, git_status_porcelain


class GitFilesGotoCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = Path(self.window.extract_variables()["folder"])
        git_status_output = git_status_porcelain(cwd)
        git_files = get_git_files(git_status_output)

        if len(git_files) > 0:
            self.window.show_quick_panel(
                items=self.to_quick_panel_item(git_files),
                on_select=partial(self.on_select, cwd, git_files),
                on_highlight=partial(self.on_highlight, cwd, git_files),
            )
        else:
            sublime.message_dialog("GitFiles: No changed files.")

    def to_quick_panel_item(self, git_files):
        return [
            sublime.QuickPanelItem(
                item.file_name,
                item.file_path,
                item.git_status,
                GIT_STATUS_KIND_MAPPING.get(
                    item.git_status,
                    (sublime.KIND_ID_AMBIGUOUS, item.git_status.lower(), ""),
                ),
            )
            for item in git_files
        ]

    def on_select(self, cwd, items, index: int):
        if index > -1:
            full_path = Path(cwd, items[index].file_path)
            if full_path.is_file():
                self.window.open_file(str(full_path))

    def on_highlight(self, cwd, items, index: int):
        if index > -1:
            full_path = Path(cwd, items[index].file_path)
            if full_path.is_file():
                self.window.open_file(str(full_path), sublime.NewFileFlags.TRANSIENT)
