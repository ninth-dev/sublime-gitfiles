import re
from pathlib import Path, PurePath
from subprocess import PIPE, Popen
from typing import List

import sublime

from .typings import GitFile

KIND_ADDED = (sublime.KIND_ID_COLOR_GREENISH, "a", "Added")
KIND_CONFLICTED = (sublime.KIND_ID_COLOR_REDISH, "c", "Conflicted")
KIND_MODIFIED = (sublime.KIND_ID_COLOR_ORANGISH, "m", "Modified")
KIND_UNTRACKED = (sublime.KIND_ID_COLOR_BLUISH, "?", "Untracked")

GIT_STATUS_KIND_MAPPING = {
    "A": KIND_ADDED,
    "C": KIND_CONFLICTED,
    "M": KIND_MODIFIED,
    "?": KIND_UNTRACKED,
}


def git_status_porcelain(cwd: Path) -> str:
    cmd = "git status --porcelain=v1"
    p = Popen(
        cmd,
        bufsize=-1,
        cwd=str(cwd),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
    )
    output, stderr = p.communicate()

    if stderr:
        print(
            f'GitFiles: An error happened while running this command "{cmd}".',
            stderr,
        )
        raise Exception(
            f'GitFiles: An error happened while running this command "{cmd}". {stderr}'
        )

    return output.decode("utf-8")


def get_git_files(status_output: str) -> List[GitFile]:
    items = []
    for result in status_output.strip().split("\n"):
        match = re.search(r"^(.?)(.?)\s(.+)", result)
        if match is None:
            return items

        index_status = match.group(1)
        working_tree_status = match.group(2)
        file_path = match.group(3)
        file_name = PurePath(file_path).name

        # GitStatus: returns the status of the index and the status of the working tree
        #  See: https://git-scm.com/docs/git-status
        if index_status == "?" and working_tree_status == "?":
            items.append(GitFile(file_name, file_path, "?"))
        elif working_tree_status == "M" or index_status == "M":
            items.append(GitFile(file_name, file_path, "M"))
        elif working_tree_status == "D":
            pass
        elif working_tree_status == "U":
            items.append(GitFile(file_name, file_path, "C"))
        elif index_status == "A":
            items.append(GitFile(file_name, file_path, "A"))
        elif index_status != " ":
            # something got staged
            pass

    return items
