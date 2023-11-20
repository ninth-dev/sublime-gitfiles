import re
from pathlib import Path, PurePath
from subprocess import PIPE, Popen
from typing import List

from .typings import GitFile, GitFileStatus


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

        items.append(
            GitFile(
                file_name, file_path, GitFileStatus(index_status, working_tree_status)
            )
        )

    return items
