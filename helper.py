import csv
import logging
from pathlib import Path

from config import DEFAULT
from model import Dependency


def write_to_csv_file(file_path: Path, dictionaries: list[dict] | None = None) -> None:
    """write extracted dependencies to a CSV file"""

    logging.info("Writing {count} dependencies to '{path}'".format(count=len(dictionaries), path=file_path))

    if not dictionaries:
        logging.warning("No data to write.")
        return

    with open(file=file_path, mode="w", encoding=DEFAULT.get("encoding"), newline="\n") as opened_file:
        writer = csv.writer(opened_file, delimiter=DEFAULT.get("delimiter"))
        keys: list[str] = list(dictionaries[0].keys())
        header = [key.lower() for key in keys]
        writer.writerow(header)
        for dictionary in dictionaries:
            row = [dictionary.get(key, "") for key in keys]
            writer.writerow(row)

        logging.info("Successfully wrote {count} dependencies to '{path}'".format(count=len(dictionaries), path=file_path))


def convert_to_dictionary(dependency: Dependency) -> dict:
    """convert dependency object to dictionary"""
    return {
        "file": dependency.file,
        "element": dependency.element,
        "attribute": dependency.attribute,
        "path": dependency.path
    }


def generate_attribute_filter_xpath(attributes: frozenset[str] | None = None) -> str:
    """generates XPath for attribute filtering"""
    attribute_filter: str = ".//@*"

    if not attributes:
        return attribute_filter

    attribute_filter += "["

    conditions = []
    for attribute in attributes:
        condition: str = "contains(local-name(.), '{attribute}')".format(attribute=attribute)
        conditions.append(condition)

    attribute_filter += " or ".join(conditions) + "]"

    return attribute_filter


def generate_element_filter_xpath(elements: frozenset[str] | None = None) -> str:
    """generates XPath for element filtering"""
    element_filter: str = ".//*"

    if not elements:
        return element_filter

    element_filter += "["

    conditions = []
    for element in elements:
        condition: str = "contains(name(.), '{element}')".format(element=element)
        conditions.append(condition)

    element_filter += " or ".join(conditions) + "]"

    return element_filter
