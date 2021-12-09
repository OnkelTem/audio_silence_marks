from enum import Enum
import subprocess
import re
import os
import typer
from pathlib import Path
from typing import List
from audio_silence_marks.types import FileInfo
from .targets.audipo import Audipo


class Target(str, Enum):
    audipo = "audipo"


def get_file_intervals(
    file: Path, noise: int = 50, duration: int = 1000
) -> List[List[int]]:
    proc = subprocess.run(
        [
            "ffmpeg",
            "-i",
            file,
            "-af",
            f"silencedetect=n=-{noise}dB:d={duration/1000}",
            "-f",
            "null",
            "-",
        ],
        check=True,
        encoding="utf-8",
        text=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    state = 0
    intervals = []
    pair = [0, 0]
    for line in proc.stderr.splitlines():
        if re_line.match(line):
            matches = re_parts[state].findall(line)
            if matches:
                pair[state] = int(float(matches[0][0]) * 1000)
                if state == 1:
                    intervals.append(pair)
                    pair = [0, 0]
                state = 1 if state == 0 else 0
            else:
                raise ValueError(f"Parsing error at: {line}")
    return intervals


def log(msg) -> None:
    typer.secho(msg, fg=typer.colors.WHITE, nl=False, err=True)


def err(msg) -> None:
    typer.secho(msg, fg=typer.colors.RED, nl=False, err=True)


def main(path, glob, target, noise: int, duration: int, lst) -> None:
    p = Path(path)
    g = p.glob(glob)
    files_info: List[FileInfo] = []
    if lst:
        for x in g:
            if x.is_file():
                typer.echo(x.relative_to(path))
        return
    for x in g:
        if x.is_file():
            log(f"File: {x}... ")
            try:
                intervals = get_file_intervals(x, noise, duration)
                files_info.append(
                    {
                        "path": x.parent.relative_to(path),
                        "file": x.name,
                        "size": os.path.getsize(x),
                        "intervals": intervals,
                    }
                )
                log(f"processed {len(intervals)} intervals\n")
            except ValueError as err:
                log(f"(skipped) Error: {err}\n")
    if target == "audipo":
        Audipo(files_info)


re_line = re.compile(r"^\[silencedetect")
re_parts = [
    re.compile(r"\bsilence_start: (\d+(\.\d+)?)$"),
    re.compile(r"\bsilence_end: (\d+(\.\d+)?)"),
]
