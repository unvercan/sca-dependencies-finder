import os

from lxml import etree as xml_parser

from dependencies_result import DependenciesResult
from dependency import Dependency
from helper import convert_dictionaries_to_csv, check_file_exists


# find dependencies
def find_dependencies(root):
    # sca files
    xml_file_extensions = [
        'wsdl',
        'xsd',
        'xml',
        'xsl',
        'bpel',
        'componentType',
        'decs',
        'dvm',
        'jpr',
        'edl',
        'jca',
        'jws',
        'config',
        'monitor',
        'mwp',
        'rules',
        'sch',
        'schema',
        'table',
        'offlinedb'
    ]

    # elements and attributes
    element_filters = [
        'reference',
        'component',
        'service',
        'import',
        'schemaImport',
        'schema-import',
        'schema'
    ]

    attribute_filters = [
        'location',
        'wsdlLocation',
        'schemaLocation',
        'localPart',
        'src'
    ]

    # generate XPaths
    element_xpath = './/*[' + ' or '.join([
        "contains(name(.),'" + element_filter + "')"
        for element_filter in element_filters
    ]) + ']'
    attribute_xpath = './/@*[' + ' or '.join([
        "contains(local-name(.),'" + attribute_filter + "')"
        for attribute_filter in attribute_filters
    ]) + ']'

    # loop over directories
    dependencies = []
    for directory_path, directory_names, file_names in os.walk(root):
        # loop over files in the same directory
        for file_name in file_names:
            # get file extension
            file_extension = ''
            if len(file_name.split('.')) > 1:
                file_extension = file_name.split('.')[-1]
            # file extension filter
            if file_extension in xml_file_extensions:
                # parse xml file
                file_path = os.path.join(directory_path, file_name)
                relative_file_path = os.path.relpath(file_path, root)
                xml_tree = xml_parser.parse(file_path)
                # get elements
                elements = xml_tree.xpath(element_xpath)
                for element in elements:
                    # get element name
                    element_name = element.xpath('name(.)')
                    # remove namespace from element name if exists
                    if len(element_name.split(':')) > 1:
                        element_name = element_name.split(':')[-1]
                    # get attributes
                    paths = element.xpath(attribute_xpath)
                    for path in paths:
                        # get attribute name
                        attribute_name = element.xpath("local-name(.//@*[. = '" + path + "'])")
                        # remove namespace from attribute name if exists
                        if len(attribute_name.split(':')) > 1:
                            attribute_name = attribute_name.split(':')[-1]
                        # ignore wsdl service location
                        if not ((file_extension == 'wsdl') and
                                (element_name == 'service') and
                                (attribute_name == 'location')):
                            # create dependency
                            dependency = Dependency(file=relative_file_path, element=element_name,
                                                    attribute=attribute_name, path=path)
                            dependencies.append(dependency)
    # return
    return dependencies


def separate_dependencies(root, dependencies, custom_filters=None):
    # dependency filters
    mds_dependency_filters = ['oramds:/']
    http_dependency_filters = ['http:/', 'https:/']
    file_dependency_filters = ['file:/']

    # separated dependencies lists
    mds_dependencies = []
    http_dependencies = []
    file_dependencies = []
    local_dependencies = []
    for dependency in dependencies:
        # check mds dependency
        if any(mds_dependency_filter in dependency.path for mds_dependency_filter in mds_dependency_filters):
            mds_dependencies.append(dependency)
        # check http dependency
        elif any(http_dependency_filter in dependency.path for http_dependency_filter in http_dependency_filters):
            http_dependencies.append(dependency)
        # check file dependency
        elif any(file_dependency_filter in dependency.path for file_dependency_filter in file_dependency_filters):
            file_dependencies.append(dependency)
        # check local dependency if path exists
        else:
            try:
                file_path = os.path.join(root, dependency.file)
                directory_path = os.path.abspath(os.path.join(file_path, '..'))
                possible_file_path = os.path.join(directory_path, dependency.path)
                if check_file_exists(possible_file_path):
                    local_dependencies.append(dependency)
            except Exception:
                pass

    # separated dependencies
    separated_dependencies = [
        DependenciesResult(category='mds', dependencies=mds_dependencies),
        DependenciesResult(category='http', dependencies=http_dependencies),
        DependenciesResult(category='file', dependencies=file_dependencies),
        DependenciesResult(category='local', dependencies=local_dependencies),
        DependenciesResult(category='all', dependencies=dependencies)
    ]

    # find custom dependency if custom filters are given
    if custom_filters:
        custom_dependencies = []
        for dependency in dependencies:
            if any(custom_filter in dependency.path for custom_filter in custom_filters):
                custom_dependencies.append(dependency)
        separated_dependencies.append(DependenciesResult(category='custom', dependencies=custom_dependencies))

    # return
    return separated_dependencies


# main
def main():
    # output files
    output_dictionary_path = os.path.dirname(os.path.realpath(__file__))
    output_files_extension = "csv"

    # sca setting
    sca_root = 'root'

    # dependencies list
    dependencies = find_dependencies(root=sca_root)

    # sort dependencies by file name
    dependencies = sorted(dependencies, key=lambda dependency: dependency.path)

    # custom filters
    custom_filters = [
        'custom_value_1',
        'custom_value_2'
    ]

    # separate dependencies
    results = separate_dependencies(root=sca_root, dependencies=dependencies, custom_filters=custom_filters)

    # create excel files for each dependencies result
    for result in results:
        if len(result.dependencies) > 0:
            output_file_name = result.category + '_dependencies' + '.' + output_files_extension
            output_file = os.path.join(output_dictionary_path, output_file_name)
            dictionaries = [dependency.convert_to_dictionary() for dependency in result.dependencies]
            number_of_dependencies = len(dictionaries)
            convert_dictionaries_to_csv(output_file=output_file, dictionaries=dictionaries)
            info = "'{output_file}' is created with {number_of_dependencies} {category} dependencies."
            print(info.format(number_of_dependencies=number_of_dependencies,
                              output_file=output_file, category=result.category))


if __name__ == '__main__':
    main()
