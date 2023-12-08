from pathlib import Path

import sublime_plugin

from ..core.git import git_status_porcelain
from ..core.modification import get_current_file, get_prev_git_file, get_relative_path
from ..core.parser import parse_git_status


class GitFilesPrevModificationCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        cwd = Path(window.extract_variables()["folder"])
        view = window.active_view()
        if view is not None:
            position = view.sel()[0].a
            window.run_command("prev_modification")
            if len(view.sel()) == 1:
                current_position = view.sel()[0].a
                # reached the top of modifications on the current file
                if current_position >= position:
                    window.run_command("next_modification")

                    output = git_status_porcelain(cwd)
                    git_files = parse_git_status(output)
                    current_file = get_current_file(window, cwd)

                    prev_git_file = get_prev_git_file(cwd, git_files, current_file)

                    if prev_git_file is not None:
                        active_view = window.open_file(str(prev_git_file))
                        active_view.run_command("prev_modification")
