import os

from lxml import etree as xml_parser

from config import ATTRIBUTES, FILE_EXTENSIONS, ELEMENTS
from helper import convert_dictionaries_to_csv, check_path_exists, check_file_exists, convert_dependency_to_dictionary, generate_element_filter_xpath, generate_attribute_filter_xpath
from model import Dependency, Result, Category


def extract_dependencies(root: str) -> list[Dependency]:
    """extract dependencies"""

    dependencies: list[Dependency] = []

    # generate filters
    element_filter: str = generate_element_filter_xpath(elements=ELEMENTS)
    attribute_filter: str = generate_attribute_filter_xpath(attributes=ATTRIBUTES)

    # loop over directories
    files: list[tuple[str, str, str]] = []
    for directory_path, directory_names, file_names in os.walk(top=root, topdown=True):
        for file_name in file_names:
            file_extension: str = ""
            if len(file_name.split(".")) > 1:
                file_extension: str = file_name.split(".")[-1]
            if file_extension in FILE_EXTENSIONS:
                file_path: str = os.path.join(directory_path, file_name)
                relative_file_path: str = os.path.relpath(path=file_path, start=root)
                file: tuple[str, str, str] = file_path, relative_file_path, file_extension
                files.append(file)

    # filter by elements and attributes
    for file_path, relative_file_path, file_extension in files:
        xml_tree = xml_parser.parse(source=file_path)
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
                if not ((file_extension == "wsdl") and (element_name == "service") and (attribute_name == "location")):
                    dependency: Dependency = Dependency(file=relative_file_path, element=element_name, attribute=attribute_name, path=path)
                    dependencies.append(dependency)

    return dependencies


def generate_results(root: str, dependencies: list[Dependency], custom_filters=list[str] | None) -> list[Result]:
    # dependency filters
    mds_filters: list[str] = [
        "oramds:/"
    ]

    http_filters: list[str] = [
        "http:/",
        "https:/"
    ]

    file_filters: list[str] = [
        "file:/"
    ]

    # separated dependencies
    mds_dependencies: list[Dependency] = []
    http_dependencies: list[Dependency] = []
    file_dependencies: list[Dependency] = []
    local_dependencies: list[Dependency] = []
    for dependency in dependencies:
        if any(mds_filter in dependency.path for mds_filter in mds_filters):
            mds_dependencies.append(dependency)
        elif any(http_filter in dependency.path for http_filter in http_filters):
            http_dependencies.append(dependency)
        elif any(file_filter in dependency.path for file_filter in file_filters):
            file_dependencies.append(dependency)
        else:
            try:
                file_path: str = os.path.join(root, dependency.file)
                directory_path: str = os.path.join(file_path, "..")
                directory_path = os.path.abspath(path=directory_path)
                possible_file_path: str = os.path.join(directory_path, dependency.path)
                if check_path_exists(path=possible_file_path) and check_file_exists(path=possible_file_path):
                    local_dependencies.append(dependency)
            except FileNotFoundError:
                pass

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
    other_dependencies: list[Dependency] = [dependency for dependency in dependencies]
    for separated in results:
        for dependency in separated.dependencies:
            if dependency in other_dependencies:
                other_dependencies.remove(dependency)
    other_result: Result = Result(category=Category.OTHER, dependencies=other_dependencies)
    results.append(other_result)

    return results


def main() -> None:
    # output
    script_file_path: str = os.path.realpath(filename=__file__)
    output_dictionary_path: str = os.path.dirname(script_file_path)
    output_files_extension: str = "csv"

    # sca
    sca_root_path: str = "root"

    # extract dependencies
    dependencies: list[Dependency] = extract_dependencies(root=sca_root_path)

    # sort dependencies
    dependencies: list[Dependency] = sorted(dependencies, key=lambda dependency: dependency.path)

    # custom filters
    custom_filters: list[str] = [
        "custom_value_1",
        "custom_value_2"
    ]

    # generate results
    results: list[Result] = generate_results(root=sca_root_path, dependencies=dependencies, custom_filters=custom_filters)

    # create excel files for each dependencies result
    for result in results:
        if len(result.dependencies) > 0:
            output_file_name: str = result.category.name + "_dependencies" + "." + output_files_extension
            output_file_path: str = os.path.join(output_dictionary_path, output_file_name)
            dictionaries: list[dict] = [convert_dependency_to_dictionary(dependency) for dependency in result.dependencies]
            convert_dictionaries_to_csv(output_file=output_file_path, dictionaries=dictionaries)
            info = "'{output_file}' is created with {number_of_dependencies} {category} dependencies."
            print(info.format(number_of_dependencies=len(dictionaries), output_file=output_file_path, category=result.category))


if __name__ == "__main__":
    main()
