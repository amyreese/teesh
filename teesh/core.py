# Copyright Amethyst Reese
# Licensed under the MIT license

import sys
from collections.abc import Sequence
from dataclasses import dataclass
from io import StringIO, TextIOBase
from pathlib import Path
from subprocess import PIPE, Popen
from threading import Thread


def stream_follower(source: TextIOBase, buffer: StringIO, output: TextIOBase) -> None:
    """Run this in a thread to follow a source stream and tee to stdout/err and io"""

    for line in source:
        buffer.write(line)
        output.write(line)
        output.flush()

    source.close()
    buffer.seek(0)


@dataclass
class CompletedProcess:
    cmd: Sequence[str | Path]
    returncode: int
    stdout: str
    stderr: str


@dataclass
class CalledProcessError(Exception):
    cmd: Sequence[str | Path] = ()
    returncode: int = -1
    stdout: str = ""
    stderr: str = ""

    def __str__(self):
        return (
            f"Command '{self.cmd[0]}' returned non-zero exit status {self.returncode}."
        )


def run(*cmd: str | Path, check: bool = True) -> CompletedProcess:
    """Run a command, and capture stdout/stderr while also passing it to the console"""

    cmd: tuple[str, ...] = tuple(str(arg) for arg in cmd)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, text=True)

    stdout_buffer = StringIO()
    stdout_follower = Thread(
        target=stream_follower, args=(proc.stdout, stdout_buffer, sys.stdout)
    )
    stdout_follower.daemon = True
    stdout_follower.start()

    stderr_buffer = StringIO()
    stderr_follower = Thread(
        target=stream_follower, args=(proc.stderr, stderr_buffer, sys.stderr)
    )
    stderr_follower.daemon = True
    stderr_follower.start()

    returncode = proc.wait()
    stdout_follower.join()
    stderr_follower.join()

    if check and returncode != 0:
        raise CalledProcessError(
            cmd=cmd,
            returncode=returncode,
            stdout=stdout_buffer.read(),
            stderr=stderr_buffer.read(),
        )

    return CompletedProcess(
        cmd=cmd,
        returncode=returncode,
        stdout=stdout_buffer.read(),
        stderr=stderr_buffer.read(),
    )
