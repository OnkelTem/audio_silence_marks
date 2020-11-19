from pathlib import Path
from typing import List, TypedDict


class FileInfo(TypedDict):
    path: Path
    file: str
    size: int
    intervals: List[List[int]]
