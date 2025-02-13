# SCA Dependencies Finder

## Overview
The **SCA Dependencies Finder** is a Python-based tool designed to parse XML files, extract dependencies based on predefined filters, and categorize them. The extracted dependencies are saved in CSV format for further analysis.

## Features
- Extracts dependencies from XML-based files (e.g., `.wsdl`, `.xsd`, `.xml`, etc.)
- Filters dependencies based on specific XML elements and attributes
- Categorizes dependencies into different types (MDS, HTTP, FILE, LOCAL, and CUSTOM)
- Supports custom filtering options
- Outputs extracted data as CSV files

## Installation
### Prerequisites
- Python 3.9+
- Install required dependencies using:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
To process a directory of XML files and extract dependencies, run:
```sh
python app.py
```
By default, the script will use the configured input and output directories specified in `config.py`.

### Custom Arguments
You can specify custom input and output directories:
```sh
python app.py --input /path/to/xml/files --output /path/to/save/results
```

## Configuration
The `config.py` file contains settings for:
- **File Extensions:** XML-based file types to process
- **Elements & Attributes:** XML tags and attributes used for dependency extraction
- **Filters:** Predefined filters for categorization (MDS, HTTP, FILE, etc.)
- **Defaults:** Input/output paths, file format, and logging settings

## Output
The extracted dependencies are saved in CSV format with filenames structured as:
```
dependencies_<CATEGORY>_<TIMESTAMP>.csv
```
Each CSV file contains the following columns:
- `file` - The relative path of the source XML file
- `element` - The XML element containing the dependency
- `attribute` - The attribute in which the dependency is found
- `path` - The extracted dependency value

## Logging
The script logs its progress and errors in the console. Log levels can be adjusted in `config.py` using:
```python
logging.basicConfig(level=logging.INFO, format=DEFAULT.get("logging_format"))
```

## License
This project is open-source and available under the MIT License.

