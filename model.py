from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    MDS = "mds"
    HTTP = "http"
    FILE = "file"
    LOCAL = "local"
    CUSTOM = "custom"
    OTHER = "other"


@dataclass
class Dependency(object):
    file: str
    element: str
    attribute: str
    path: str


@dataclass
class Result(object):
    category: Category
    dependencies: list
