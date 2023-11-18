from pathlib import Path

import sublime_plugin

from ..common.git import get_git_files
from ..common.modification import get_next_git_file, get_position, get_relative_path


class GitFilesNextModificationCommand(sublime_plugin.WindowCommand):
    def run(self):
        window = self.window
        cwd = Path(window.extract_variables()["folder"])
        settings = window.settings()
        view = window.active_view()
        if view is not None:
            position = get_position(settings)
            window.run_command("next_modification")
            if len(view.sel()) == 1:
                current_position = view.sel()[0].b
                # finished the list of modification on the current file
                if current_position <= position:
                    window.run_command("prev_modification")

                    git_files = get_git_files(cwd)
                    file_path = window.extract_variables()["file"]
                    current_file = get_relative_path(cwd, file_path)
                    next_git_file = get_next_git_file(cwd, git_files, current_file)

                    if next_git_file is not None:
                        active_view = window.open_file(str(next_git_file))
                        active_view.run_command("next_modification")
                        current_position = active_view.sel()[0].b

                settings.set("gf_position", current_position)
