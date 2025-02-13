import csv
from pathlib import Path

from model import Dependency


def write_to_csv_file(file_path: Path, dictionaries: list[dict] = None) -> None:
    """generate csv file using giving dictionaries"""
    if not dictionaries:
        return

    with open(file=file_path, mode="w", encoding="utf-8", newline="\n") as opened_file:
        writer = csv.writer(opened_file, dialect="excel", delimiter=";")
        keys: list[str] = list(dictionaries[0].keys())
        header = [key.lower() for key in keys]
        writer.writerow(header)
        for dictionary in dictionaries:
            row = [dictionary.get(key, "") for key in keys]
            writer.writerow(row)


def convert_to_dictionary(dependency: Dependency) -> dict:
    """convert dependency object to dictionary"""
    return {
        "file": dependency.file,
        "element": dependency.element,
        "attribute": dependency.attribute,
        "path": dependency.path
    }


def generate_attribute_filter_xpath(attributes: frozenset[str] = None) -> str:
    """generates XPath for attribute filtering"""
    attribute_filter: str = ".//@*"

    if not attributes:
        return attribute_filter

    attribute_filter += "["

    conditions = []
    for attribute in attributes:
        condition: str = "contains(local-name(.)," + "'" + attribute + "')"
        conditions.append(condition)

    attribute_filter += " or ".join(conditions) + "]"

    return attribute_filter


def generate_element_filter_xpath(elements: frozenset[str] = None) -> str:
    """generates XPath for element filtering"""
    element_filter: str = ".//*"

    if not elements:
        return element_filter

    element_filter += "["

    conditions = []
    for element in elements:
        condition: str = "contains(name(.)," + "'" + element + "')"
        conditions.append(condition)

    element_filter += " or ".join(conditions) + "]"

    return element_filter
