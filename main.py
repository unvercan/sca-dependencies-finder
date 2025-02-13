import argparse
import logging

from app import process
from config import DEFAULT

if __name__ == "__main__":
    # configure logging
    logging.basicConfig(level=logging.INFO, format=DEFAULT["logging_format"])

    # command-line argument parser
    parser = argparse.ArgumentParser()

    # parsing command-line arguments
    parser.add_argument("-i", "--input", type=str, default=DEFAULT.get("input"), help="path to input folder")
    parser.add_argument("-o", "--output", type=str, default=DEFAULT.get("output"), help="path to output folder")
    parser.add_argument("-p", "--prefix", type=str, default=DEFAULT.get("prefix"), help="output name prefix")

    arguments = parser.parse_args()

    logging.info("Arguments: input='{input}' output:'{output}' prefix:'{prefix}'".format(input=arguments.input, output=arguments.output, prefix=arguments.prefix))

    # process
    process(input_folder_path=arguments.input, output_folder_path=arguments.output, output_prefix=arguments.prefix)
