import os
from lxml import etree as xml_parser
import csv

# output file
output_file_name = "output"
output_file_extension = "csv"
output_file_path = os.path.dirname(os.path.realpath(__file__))
output_file = os.path.join(output_file_path, (output_file_name + '.' + output_file_extension))

# sca setting
sca_root = "sca_root"
sca_composite_1 = os.path.join(sca_root, "sca_composite_1")
sca_composite_2 = os.path.join(sca_root, "sca_composite_2")
sca_composite_3 = os.path.join(sca_root, "sca_composite_3")
sca_composites = [sca_composite_1, sca_composite_2, sca_composite_3]
sca_file_extensions = ["jws", "xml", "jpr", "bpel", "wsdl", "xsd", "xsl", "mplan", "componentType", "jca", "monitor", "config", "decs", "rules"]

# elements and attributes
element_filters = ["reference", "import"]
attribute_filters = ['location', 'wsdlLocation', 'schemaLocation']
value_filters = ['value_1', 'value_2', 'value_3']

# result list
results = []

# loop over composites
for sca_composite in sca_composites:
    # loop over directories
    for directory_path, directory_names, file_names in os.walk(sca_composite):
        # loop over files in the same directory
        for file_name in file_names:
            # get file extension
            file_extension = ""
            if len(file_name.split('.')) > 1:
                file_extension = file_name.split('.')[-1]
            # file extension filter
            if file_extension in sca_file_extensions:
                file_path = os.path.join(directory_path, file_name)
                xml_tree = xml_parser.parse(file_path)
                # create value filters
                filters = " or ".join(["contains(., '{filter}')".format(filter=value_filter) for value_filter in value_filters])
                # get elements
                elements = xml_tree.xpath(".//*[./@*[{filters}]]".format(filters=filters))
                for element in elements:
                    # get element name
                    element_name = element.xpath("name(.)")
                    # filter element
                    if element_name in element_filters:
                        # remove namespace from element name if exists
                        if len(element_name.split(':')) > 1:
                            element_name = element_name.split(':')[-1]
                        # get attributes
                        paths = element.xpath("./@*[{filters}]".format(filters=filters))
                        for path in paths:
                            # get attribute name
                            attribute_name = element.xpath("local-name(./@*[. = '{path}'])".format(path=path))
                            # remove namespace from attribute name if exists
                            if len(attribute_name.split(':')) > 1:
                                attribute_name = attribute_name.split(':')[-1]
                            # filter attribute
                            if attribute_name in attribute_filters:
                                results.append({"file": os.path.relpath(file_path, sca_root), "element": element_name, "attribute": attribute_name, "path": path})

# create output file
with open(file=output_file, mode='w', encoding='utf-8', newline='\n') as opened_file:
    # check number of results
    if len(results) > 0:
        csv_writer = csv.writer(opened_file, delimiter=';')
        # output file header
        header = [key.title() for key in list(results[0].keys())]
        # print header
        csv_writer.writerow(header)
        # loop over results
        for result in results:
            # output file data
            data = result.values()
            # print data
            csv_writer.writerow(data)
        # print success message with results
        print("'{output_file}' is created with {number_of_results} results.".format(output_file=output_file, number_of_results=len(results)))
    else:
        # print success message without results
        print("There is no result.")
