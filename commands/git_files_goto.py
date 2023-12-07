import re
from functools import partial
from pathlib import Path
from typing import List, Optional

import sublime
import sublime_plugin

from ..core.git import git_status_porcelain
from ..core.parser import parse_git_status
from ..core.typings import GitFile


class GitFilesGotoCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = Path(self.window.extract_variables()["folder"])
        output = git_status_porcelain(cwd)
        git_files = parse_git_status(output)

        active_view = self.window.active_view()
        self._highlighted_view = None  # type: Optional[sublime.View]

        if len(git_files) > 0:
            self.window.show_quick_panel(
                items=self.to_quick_panel_item(git_files),
                on_select=partial(self.on_select, active_view, cwd, git_files),
                on_highlight=partial(self.on_highlight, cwd, git_files),
            )
        else:
            sublime.message_dialog("GitFiles: No changed files.")

    def to_quick_panel_item(
        self, git_files: List[GitFile]
    ) -> List[sublime.QuickPanelItem]:
        items = []
        for item in git_files:
            git_status = item.git_status
            items.append(
                sublime.QuickPanelItem(
                    item.file_name,
                    item.file_path,
                    git_status.description(),
                    git_status.kind(),
                )
            )
        return items

    def __open_file(
        self, cwd, items, index: int, on_highlight: bool
    ) -> Optional[sublime.View]:
        if index == -1:
            return None

        rename_match = re.search(r"(.+) -> (.*)", items[index].file_path)
        file_path = (
            rename_match.group(2)
            if rename_match is not None
            else items[index].file_path
        )
        full_path = Path(cwd, file_path)
        flag = sublime.TRANSIENT if on_highlight else sublime.NewFileFlags.NONE
        if full_path.is_file():
            return self.window.open_file(
                str(full_path), flag, self.window.active_group()
            )
        return None

    def on_select(self, active_view: Optional[sublime.View], cwd, items, index: int):
        if index == -1:
            if active_view is not None and active_view.is_valid():
                self.window.focus_view(active_view)
                active_view.show(active_view.sel()[0])

            if self._highlighted_view:
                sheet = self._highlighted_view.sheet()
                if sheet and sheet.is_transient():
                    self._highlighted_view.close()

        self.__open_file(cwd, items, index, False)

    def on_highlight(self, cwd, items, index: int):
        self._highlighted_view = self.__open_file(cwd, items, index, True)
