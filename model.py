from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    MDS: str = "mds"
    HTTP: str = "http"
    FILE: str = "file"
    LOCAL: str = "local"
    CUSTOM: str = "custom"
    OTHER: str = "other"


@dataclass
class Dependency(object):
    file: str
    element: str
    attribute: str
    path: str


@dataclass
class Result(object):
    category: Category
    dependencies: list[Dependency]
