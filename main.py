import argparse

from app import run
from config import DEFAULT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, default=DEFAULT.get("input"), help="path to input folder")
    parser.add_argument("-o", "--output", type=str, default=DEFAULT.get("output"), help="path to output folder")
    parser.add_argument("-p", "--prefix", type=str, default=DEFAULT.get("prefix"), help="output name prefix")
    parser.add_argument("-f", "--format", type=str, default=DEFAULT.get("format"), help="output format")

    arguments = parser.parse_args()

    run(input_folder_path=arguments.input, output_folder_path=arguments.output, output_format=arguments.format, output_prefix=arguments.prefix)
