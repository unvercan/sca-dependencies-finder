# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:02:10 2018

@author: Ünver Can Ünlü
"""

from lxml import etree as xml_parser
from helper import dictionaries_to_csv, check_file_exists
from dependency import Dependency
from dependencies_result import DependenciesResult
import os

# find dependencies
def find_dependencies(root):
    # sca files
    xml_file_extensions = list(set(['wsdl', 'xsd', 'xml', 'xsl', 'bpel', 'componentType', 'decs', 'dvm', 'jpr', 'edl', 'jca', 'jws', 'config', 'monitor', 'mwp', 'rules', 'sch', 'schema', 'table', 'offlinedb']))
    
    # elements and attributes
    element_filters = list(set(['reference', 'component', 'service', 'import', 'schemaImport', 'schema-import', 'schema']))
    attribute_filters = list(set(['location', 'wsdlLocation', 'schemaLocation', 'localPart', 'src']))
    
    # generate xpaths
    element_xpath = './/*[' + ' or '.join(["contains(name(.),'" + element_filter + "')" for element_filter in element_filters]) + ']'
    attribute_xpath = './/@*[' + ' or '.join(["contains(local-name(.),'" + attribute_filter + "')" for attribute_filter in attribute_filters]) + ']'
    
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
                        if not((file_extension == 'wsdl') and (element_name == 'service') and (attribute_name == 'location')):
                            # create dependency
                            dependency = Dependency(file=relative_file_path, element=element_name, attribute=attribute_name, path=path)
                            dependencies.append(dependency)
    # return
    return dependencies

def seperate_dependencies(root, dependencies, custom_filters=None):
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
    seperated_dependencies = [DependenciesResult(type='mds', dependencies=mds_dependencies), DependenciesResult(type='http', dependencies=http_dependencies), DependenciesResult(type='file', dependencies=file_dependencies), DependenciesResult(type='local', dependencies=local_dependencies),DependenciesResult(type='all', dependencies=dependencies)]

    # find custom dependency if custom filters are given
    if custom_filters:
        custom_dependencies = []
        for dependency in dependencies:
            if any(custom_filter in dependency.path for custom_filter in custom_filters):
                custom_dependencies.append(dependency)
        seperated_dependencies.append(DependenciesResult(type='custom', dependencies=custom_dependencies))
    
    # return
    return seperated_dependencies

# main
def main():
    # output files
    output_files_path = os.path.dirname(os.path.realpath(__file__))
    output_files_extension = "csv"
    
    # sca setting
    sca_root = 'root'
    
    # dependencies list
    dependencies = find_dependencies(root=sca_root)
    
    # sort dependencies by file name
    dependencies = sorted(dependencies, key=lambda dependency: dependency.path)
    
    # custom filters
    custom_filters = ['custom_value_1', 'custom_value_2'] 
    
    # separate dependencies
    dependencies_results = seperate_dependencies(root=sca_root, dependencies=dependencies, custom_filters=custom_filters)

    # create excel files for each dependencies result
    for dependencies_result in dependencies_results:
        if len(dependencies_result.dependencies) > 0:
            output_file=os.path.join(output_files_path, (dependencies_result.type + '_dependencies' + '.' + output_files_extension))
            dictionaries = [dependency.as_dict() for dependency in dependencies_result.dependencies]
            number_of_dependencies = len(dictionaries)
            dictionaries_to_csv(output_file=output_file, dictionaries=dictionaries)
            print("'{output_file}' is created with {number_of_dependencies} {type} dependencies.".format(output_file=output_file, number_of_dependencies=number_of_dependencies, type=dependencies_result.type))

if __name__ == '__main__':
    main()
