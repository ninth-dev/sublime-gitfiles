from pathlib import Path
from subprocess import PIPE, Popen


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
