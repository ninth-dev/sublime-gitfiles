from typing import NamedTuple, Tuple

import sublime

from .git_status import GitStatus


class GitFile(NamedTuple):
    file_name: str
    file_path: str
    git_status: GitStatus
