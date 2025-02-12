import os
from pathlib import Path

from app import extract_dependencies, generate_results
from helper import convert_dependency_to_dictionary, write_to_csv_file
from model import Dependency, Result


def main() -> None:
    """main"""

    # output
    script_file_path = Path(__file__).resolve()
    output_directory_path = script_file_path.parent
    output_files_extension: str = "csv"

    # sca
    sca_root_path: str = "C:\\Users\\unver\\PycharmProjects\\sca-dependencies-finder"

    # extract dependencies
    dependencies: list[Dependency] = extract_dependencies(root=sca_root_path)

    # sort dependencies
    dependencies = sorted(dependencies, key=lambda dependency: dependency.path)

    # custom filters
    custom_filters: frozenset[str] = frozenset({
        "custom_value_1",
        "custom_value_2"
    })

    # generate results
    results: list[Result] = generate_results(root=sca_root_path, dependencies=dependencies, custom_filters=custom_filters)

    # create excel files for each dependencies result
    for result in results:
        if result.dependencies:
            output_file_name: str = result.category.name + "_dependencies" + "." + output_files_extension
            output_file_path: str = os.path.join(output_directory_path, output_file_name)
            dictionaries: list[dict] = [convert_dependency_to_dictionary(dependency) for dependency in result.dependencies]
            write_to_csv_file(output_file=output_file_path, dictionaries=dictionaries)
            info = "'{output_file}' is created with {number_of_dependencies} {category} dependencies."
            print(info.format(number_of_dependencies=len(dictionaries), output_file=output_file_path, category=result.category))


if __name__ == "__main__":
    main()
