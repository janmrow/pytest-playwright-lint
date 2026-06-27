from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    col: int
    code: str
    message: str
    url: str = ""
