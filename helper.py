import csv
from pathlib import Path

from model import Dependency, Result


def convert_dictionaries_to_csv(output_file: str, dictionaries: list[dict] = ()) -> None:
    """generate csv file using giving dictionaries"""
    with open(file=output_file, mode="w", encoding="utf-8", newline="\n") as opened_file:
        if len(dictionaries) > 0:
            csv_writer = csv.writer(opened_file, dialect="excel", delimiter=";")
            header = [key.title() for key in list(dictionaries[0].keys())]
            csv_writer.writerow(header)
            for dictionary in dictionaries:
                data = dictionary.values()
                csv_writer.writerow(data)


def check_path_exists(path: str) -> bool:
    """check given path exists"""
    possible_file = Path(path)
    return possible_file.exists()


def check_file_exists(path: str) -> bool:
    """check file exists in given path"""
    possible_file = Path(path)
    return possible_file.is_file()


def convert_dependency_to_dictionary(dependency: Dependency) -> dict:
    """convert dependency object to dictionary"""
    return dict(file=dependency.file, element=dependency.element, attribute=dependency.attribute, path=dependency.path)


def convert_result_to_dictionary(result: Result) -> dict:
    """convert result object to dictionary"""
    return dict(type=result.category, dependencies=result.dependencies)


def generate_attribute_filter_xpath(attributes: list[str] = ()) -> str:
    """generates XPath for attribute filtering"""
    attribute_filter: str = ".//@*["
    for i in range(len(attributes)):
        attribute_filter += "contains(local-name(.),"
        attribute_filter += "'" + attributes[i] + "')"
        if i != len(attributes) - 1:
            attribute_filter += " or "
    attribute_filter += "]"
    return attribute_filter


def generate_element_filter_xpath(elements: list[str] = ()) -> str:
    """generates XPath for element filtering"""
    element_filter: str = ".//*["
    for i in range(len(elements)):
        element_filter += "contains(name(.),"
        element_filter += "'" + elements[i] + "')"
        if i != len(elements) - 1:
            element_filter += " or "
    element_filter += "]"
    return element_filter
