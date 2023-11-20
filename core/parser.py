import re
from pathlib import PurePath
from typing import List

from .typings import GitFile, GitFileStatus


def parse_git_status(status_output: str) -> List[GitFile]:
    items = []
    for result in status_output.split("\n"):
        match = re.search(r"^(.?)(.?)\s(.+)", result)
        if match is None:
            return items

        index_status = match.group(1)
        working_tree_status = match.group(2)
        file_path = match.group(3)
        file_name = PurePath(file_path).name

        items.append(
            GitFile(
                file_name,
                file_path,
                GitFileStatus(index_status, working_tree_status),
            )
        )

    return items
