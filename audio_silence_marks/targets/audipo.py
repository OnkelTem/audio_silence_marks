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


class Audipo:
    def __init__(self, files_info: List[FileInfo]):
        output = {
            "externalStorageDirectory": "",
            "files": [Audipo.process_file(file_info) for file_info in files_info],
        }
        print(json.dumps(output))

    @staticmethod
    def process_file(file_info: FileInfo) -> AudipoFile:
        return {
            "fileSize": file_info["size"],
            "filepath": Audipo.process_file_path(file_info),
            "marklist": [
                Audipo.process_mark(i, x) for i, x in enumerate(file_info["intervals"])
            ],
        }

    @staticmethod
    def process_mark(index: int, interval: List[int]) -> AudipoMark:
        diff = interval[1] - interval[0]
        return {
            "id": index,
            "pos": interval[1] - 500 if diff > 1000 else interval[0] + int(diff / 2),
        }

    @staticmethod
    def process_file_path(file_info: FileInfo):
        path = str(file_info["path"])
        file = str(file_info["file"])
        if path == ".":
            path = "/"
        else:
            path = "/" + path + "/"
        return path + file
