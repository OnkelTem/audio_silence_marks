import json
from typing import List, TypedDict
from audio_silence_marks.types import FileInfo


class AudipoMark(TypedDict):
    id: int
    pos: int


class AudipoFile(TypedDict):
    fileSize: int
    filepath: str
    marklist: List[AudipoMark]


class AudipoMarks(TypedDict):
    externalStorageDirectory: str
    files: List[AudipoFile]


def output_audipo_file_mark(index: int, interval: List[int]) -> AudipoMark:
    diff = interval[1] - interval[0]
    return {
        "id": index,
        "pos": interval[1] - 500 if diff > 1000 else interval[0] + int(diff / 2),
    }


def output_audipo_file(file_info: FileInfo) -> AudipoFile:
    return {
        "fileSize": file_info["size"],
        "filepath": str(file_info["path"])
        + ("/" if file_info["path"] else "")
        + str(file_info["file"]),
        "marklist": [
            output_audipo_file_mark(i, x) for i, x in enumerate(file_info["intervals"])
        ],
    }


def main(files_info: List[FileInfo]) -> None:
    output = {
        "externalStorageDirectory": "/storage/emulated/0",
        "files": [output_audipo_file(file_info) for file_info in files_info],
    }
    print(json.dumps(output))
