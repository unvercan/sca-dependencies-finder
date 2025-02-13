from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Category(Enum):
    MDS: str = "mds"
    HTTP: str = "http"
    FILE: str = "file"
    LOCAL: str = "local"
    CUSTOM: str = "custom"
    OTHER: str = "other"


@dataclass
class Dependency(object):
    file: Path
    element: str
    attribute: str
    path: str


@dataclass
class Result(object):
    category: Category
    dependencies: list[Dependency]
