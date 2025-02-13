import os
from datetime import datetime
from pathlib import Path

from lxml import etree as xml_parser
from lxml.etree import XPathEvalError

from config import FILE_EXTENSIONS, IGNORES, DEFAULT, MDS_FILTERS, HTTP_FILTERS, FILE_FILTERS
from helper import generate_element_filter_xpath, generate_attribute_filter_xpath, convert_to_dictionary, write_to_csv_file
from model import Dependency, Result, Category


def extract_dependencies(root: str) -> list[Dependency]:
    """extract dependencies"""

    dependencies: list[Dependency] = []

    # generate filters
    element_filter: str = generate_element_filter_xpath(elements=None)
    attribute_filter: str = generate_attribute_filter_xpath(attributes=None)

    # loop over directories
    files: list[tuple[Path, Path, str]] = []
    for directory_path, directory_names, file_names in os.walk(top=root, topdown=True):
        for file_name in file_names:
            file_path: Path = Path(directory_path) / Path(file_name)
            file_extension: str = file_path.suffix.lstrip(".")
            relative_file_path: Path = file_path.relative_to(root)
            if file_extension in FILE_EXTENSIONS:
                file: tuple[Path, Path, str] = file_path, relative_file_path, file_extension
                files.append(file)

    # filter by elements and attributes
    for file_path, relative_file_path, file_extension in files:
        xml_tree = xml_parser.parse(source=file_path)
        try:
            elements = xml_tree.xpath(element_filter)
            for element in elements:
                element_name: str = element.xpath("name(.)")
                if len(element_name.split(":")) > 1:
                    element_name: str = element_name.split(":")[-1]
                paths: list[str] = element.xpath(attribute_filter)
                for path in paths:
                    attribute_name: str = element.xpath("local-name(.//@*[. = '" + path + "'])")
                    if len(attribute_name.split(":")) > 1:
                        attribute_name: str = attribute_name.split(":")[-1]
                    if not any(file_extension == ignored_file_extension and element_name == ignored_element and attribute_name == ignored_attribute
                               for ignored_file_extension, ignored_element, ignored_attribute in IGNORES):
                        dependency: Dependency = Dependency(file=relative_file_path, element=element_name, attribute=attribute_name, path=path)
                        dependencies.append(dependency)
        except XPathEvalError as error:
            print("XPath evaluation failed: {error}".format(error=error))

    return dependencies


def generate_results(root: str, dependencies: list[Dependency] = None, custom_filters: frozenset[str] | None = None) -> list[Result]:
    """generate results"""

    # separated dependencies
    mds_dependencies: list[Dependency] = []
    http_dependencies: list[Dependency] = []
    file_dependencies: list[Dependency] = []
    local_dependencies: list[Dependency] = []
    for dependency in dependencies:
        if any(mds_filter in dependency.path for mds_filter in MDS_FILTERS):
            mds_dependencies.append(dependency)
        elif any(http_filter in dependency.path for http_filter in HTTP_FILTERS):
            http_dependencies.append(dependency)
        elif any(file_filter in dependency.path for file_filter in FILE_FILTERS):
            file_dependencies.append(dependency)
        else:
            try:
                file_path: Path = Path(root) / dependency.file
                directory_path: Path = file_path.parent
                possible_file_path: Path = directory_path / dependency.path
                if possible_file_path.exists() and possible_file_path.is_file():
                    local_dependencies.append(dependency)
            except FileNotFoundError as error:
                print("File not found: {error}".format(error=error))

    results: list[Result] = [
        Result(category=Category.MDS, dependencies=mds_dependencies),
        Result(category=Category.HTTP, dependencies=http_dependencies),
        Result(category=Category.FILE, dependencies=file_dependencies),
        Result(category=Category.LOCAL, dependencies=local_dependencies)
    ]

    # filter by custom filter if exists
    if custom_filters:
        custom_dependencies: list[Dependency] = []
        for dependency in dependencies:
            if any(custom_filter in dependency.path for custom_filter in custom_filters):
                custom_dependencies.append(dependency)
        custom_result: Result = Result(category=Category.CUSTOM, dependencies=custom_dependencies)
        results.append(custom_result)

    # other dependencies
    other_dependencies: list[Dependency] = dependencies.copy()
    for separated in results:
        for dependency in separated.dependencies:
            if dependency in other_dependencies:
                other_dependencies.remove(dependency)
    other_result: Result = Result(category=Category.OTHER, dependencies=other_dependencies)
    results.append(other_result)

    return results


def run(input_folder_path: str = DEFAULT.get("input"), output_folder_path: str = DEFAULT.get("output"), output_format: str = DEFAULT.get("prefix"), output_prefix: str = DEFAULT.get("format")) -> None:
    """run"""

    # extract dependencies
    dependencies: list[Dependency] = extract_dependencies(root=input_folder_path)

    # sort dependencies
    dependencies = sorted(dependencies, key=lambda dependency: dependency.path)

    # generate results
    results: list[Result] = generate_results(root=input_folder_path, dependencies=dependencies, custom_filters=None)

    # create csv files for each result
    for result in results:
        if result.dependencies:
            timestamp = datetime.now().strftime(DEFAULT.get("datetime_format"))
            output_file_name: str = output_prefix + "_" + result.category.name + "_" + timestamp + "." + output_format
            output_file_path: Path = Path(output_folder_path) / output_file_name
            dictionaries: list[dict] = [convert_to_dictionary(dependency) for dependency in result.dependencies]
            write_to_csv_file(file_path=output_file_path, dictionaries=dictionaries)
