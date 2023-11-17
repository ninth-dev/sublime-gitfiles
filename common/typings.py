from typing import NamedTuple

class GitFile(NamedTuple):
    file_name: str
    file_path: str
    git_status: str

