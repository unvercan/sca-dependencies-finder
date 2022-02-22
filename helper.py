# -*- coding: utf-8 -*-

import csv
from pathlib import Path


# generate csv file using giving dictionaries
def convert_dictionaries_to_csv(output_file, dictionaries):
    with open(file=output_file, mode='w', encoding='utf-8', newline='\n') as opened_file:
        number_of_dictionaries = len(dictionaries)
        if number_of_dictionaries > 0:
            csv_writer = csv.writer(opened_file, delimiter=';')
            header = [key.title() for key in list(dictionaries[0].keys())]
            csv_writer.writerow(header)
            # loop over dictionaries
            for dictionary in dictionaries:
                data = dictionary.values()
                csv_writer.writerow(data)


# check file exists in given path
def check_file_exists(path):
    possible_file = Path(path)
    return possible_file.is_file()
