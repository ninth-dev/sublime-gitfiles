from pathlib import Path

import sublime
import sublime_plugin

from ..common.git import get_git_files


class GitFilesOpenFilesCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = Path(self.window.extract_variables()["folder"])
        git_files = get_git_files(cwd)
        if len(git_files) > 0:
            for git_file in git_files:
                full_path = Path(cwd, git_file.file_path)
                if full_path.is_file():
                    self.window.open_file(str(full_path))
        else:
            sublime.message_dialog("GitFiles: No changed files.")
