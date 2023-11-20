from pathlib import Path
from typing import List, Optional

from sublime import Settings

from typing import Optional
from .typings import GitFile


def get_relative_path(folder_path: Path, full_path: str) -> str:
    return full_path.replace(f"{folder_path}/", "")


def get_next_git_file(
    cwd: Path, git_files: List[GitFile], current_file: Optional[str]
) -> Optional[Path]:
    file_list = [file.file_path for file in git_files]
    current_file_index = (
        safe_index(file_list, current_file) if current_file is not None else None
    )

    if current_file_index is None:
        next_file_index = 0
    elif current_file_index == len(file_list) - 1:
        next_file_index = 0
    else:
        next_file_index = current_file_index + 1

    next_git_file = Path(cwd, file_list[next_file_index])
    return next_git_file if next_git_file.is_file() else None


def get_prev_git_file(
    cwd: Path, git_files: List[GitFile], current_file: Optional[str]
) -> Optional[Path]:
    file_list = [file.file_path for file in git_files]
    current_file_index = (
        safe_index(file_list, current_file) if current_file is not None else None
    )

    prev_git_file_index = 0 if current_file_index is None else current_file_index - 1

    prev_git_file = Path(cwd, file_list[prev_git_file_index])

    return prev_git_file if prev_git_file.is_file() else None


def safe_index(xs: List[str], x: str) -> Optional[int]:
    try:
        return xs.index(x)
    except ValueError:
        return None
