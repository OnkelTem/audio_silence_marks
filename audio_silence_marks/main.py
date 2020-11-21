import typer
from enum import Enum
import subprocess
import re
import sys
import os
from pathlib import Path
from typing import List
from audio_silence_marks.targets import audipo
from audio_silence_marks.types import FileInfo


def cli():
    typer.run(cli_main)


class Target(str, Enum):
    audipo = "audipo"


def cli_main(
    path: Path = typer.Argument(
        ...,
        help='is a path to files. E.g: "."',
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=False,
    ),
    glob: str = typer.Argument(
        ..., help="argument is a pattern for selecting files. E.g.: '**/*.mp3'"
    ),
    target: Target = typer.Option(
        Target.audipo, "--target", "-t", help="Target format for marks."
    ),
    noise: int = typer.Option(
        50,
        "--noise",
        "-n",
        help="Maximum volume of the noise treated as silence in -dB",
    ),
    duration: int = typer.Option(
        1, "--noise", "-d", help="Minimum length of the silent interval in seconds"
    ),
    lst: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="Simply lists matched files. Useful for GLOB debugging.",
    ),
) -> None:
    """Processes audio files using FFmpeg filter silencedetect and outputs Audipo markers JSON with the list of
    spots placed in the middle of silence intervals.

    More info on using GLOBS: https://docs.python.org/3.8/library/glob.html
    """
    main(path, glob, target, noise, duration, lst)


def log(msg) -> None:
    print(msg, end="", flush=True, file=sys.stderr)


def main(path, glob, target, noise, duration, lst) -> None:
    p = Path(path)
    g = p.glob(glob)
    files_info: List[FileInfo] = []
    if lst:
        for x in g:
            if x.is_file():
                print(x.relative_to(path))
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
        audipo.main(files_info)


re_line = re.compile(r"^\[silencedetect")
re_parts = [
    re.compile(r"\bsilence_start: (\d+(\.\d+)?)$"),
    re.compile(r"\bsilence_end: (\d+(\.\d+)?)"),
]


def get_file_intervals(
    file: Path, noise: int = 50, duration: int = 1
) -> List[List[int]]:
    proc = subprocess.run(
        [
            "ffmpeg",
            "-i",
            file,
            "-af",
            f"silencedetect=n=-{noise}dB:d={duration}",
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
