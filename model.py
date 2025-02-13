from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# enum for dependency categories
class Category(Enum):
    MDS: str = "mds"
    HTTP: str = "http"
    FILE: str = "file"
    LOCAL: str = "local"
    CUSTOM: str = "custom"
    OTHER: str = "other"


@dataclass
class Dependency(object):
    """represents a dependency extracted from an XML file"""
    file: Path
    element: str
    attribute: str
    path: str


@dataclass
class Result(object):
    """holds dependencies categorized by type"""
    category: Category
    dependencies: list[Dependency]
