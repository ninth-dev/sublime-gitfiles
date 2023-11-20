from pathlib import Path

import sublime
import sublime_plugin

from ..core.git import git_status_porcelain
from ..core.parser import parse_git_status


class GitFilesOpenFilesCommand(sublime_plugin.WindowCommand):
    def run(self):
        cwd = Path(self.window.extract_variables()["folder"])
        output = git_status_porcelain(cwd)
        git_files = parse_git_status(output)
        if len(git_files) > 0:
            for git_file in git_files:
                full_path = Path(cwd, git_file.file_path)
                if full_path.is_file():
                    self.window.open_file(str(full_path))
        else:
            sublime.message_dialog("GitFiles: No changed files.")
