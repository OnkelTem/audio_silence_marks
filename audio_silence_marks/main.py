"""Audipo auto marker.
Usage:
  audipo-auto-marker PATH GLOB [-f FORMAT] [-l] [-n NOISE_THRESHOLD] [-d DURATION]

Processes audio file FILE using FFMPEG and outputs Audipo markers JSON with the list of
spots placed in the middle of silence intervals.

Arguments:
  PATH                Path to files. [Default: '.']
  GLOB                Glob patter for selecting files. [Default: '**/*.mp3']
                      @see: https://docs.python.org/3.8/library/glob.html
Options:
  -f FORMAT           Marks output format. [Default: audipo]
  -l                  Simply list files not doing anything. Useful for globs debugging.
  -n NOISE_THRESHOLD  Maximum volume of the noise treated as silence in dB [Default: -50]
  -d DURATION         Minimum length of the silent interval in seconds [Default: 1]

"""
import subprocess
import re
import sys
import os
from docopt import docopt
from pathlib import Path
from typing import List
from audio_silence_marks.targets import audipo
from audio_silence_marks.types import FileInfo


def main() -> None:
    args = docopt(__doc__)
    p = Path(args["PATH"])
    g = p.glob(args["GLOB"])
    files_info: List[FileInfo] = []
    if args["-l"]:
        for x in g:
            if x.is_file():
                print(x)
        return
    for x in g:
        if x.is_file():
            try:
                files_info.append(
                    {
                        "path": x.parent,
                        "file": x.name,
                        "size": os.path.getsize(x),
                        "intervals": get_file_intervals(x),
                    }
                )
            except ValueError as err:
                print(f"Skipping file {x}: {err}", file=sys.stderr)
    if args["-f"] == "audipo":
        audipo.main(files_info)


re_line = re.compile(r"^\[silencedetect")
re_parts = [
    re.compile(r"\bsilence_start: (\d+(\.\d+)?)$"),
    re.compile(r"\bsilence_end: (\d+(\.\d+)?)"),
]


def get_file_intervals(file: Path) -> List[List[int]]:
    proc = subprocess.run(
        ["ffmpeg", "-i", file, "-af", "silencedetect=n=-50dB:d=1", "-f", "null", "-"],
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
