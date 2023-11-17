import re
from pathlib import PurePath
from subprocess import PIPE, Popen

import sublime

from .typings import GitFile

KIND_ADDED = (sublime.KIND_ID_COLOR_GREENISH, "a", "Added")
KIND_MODIFIED = (sublime.KIND_ID_COLOR_ORANGISH, "m", "Modified")
KIND_UNTRACKED = (sublime.KIND_ID_COLOR_BLUISH, "?", "Untracked")

# TODO: Handle all cases of the status
# GitStatus: returns the status of the index and the status of the working tree
#  See: https://git-scm.com/docs/git-status
GIT_STATUS_KIND_MAPPING = {"A": KIND_ADDED, "M": KIND_MODIFIED, "?": KIND_UNTRACKED}


def git_status_porcelain(cwd):
    cmd = "git status --porcelain=v1"
    p = Popen(
        cmd,
        bufsize=-1,
        cwd=cwd,
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


def get_git_files(cwd):
    items = []
    for result in git_status_porcelain(cwd).strip().split("\n"):
        match = re.search(r"^(.?)(.?)\s(.+)", result)
        if match is None:
            return items

        index_status = match.group(1)
        working_tree_status = match.group(2)
        file_path = match.group(3)
        file_name = PurePath(file_path).name

        if index_status == "?" and working_tree_status == "?":
            items.append(GitFile(file_name, file_path, "?"))
        elif working_tree_status == "M":
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
