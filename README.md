# SCA Dependencies Finder

## Overview

SCA Dependencies Finder is a Python tool designed to scan directories for XML files, extract dependencies based on specific elements and attributes, categorize them, and export the results as CSV
files.

## Features

- Scans directories recursively for XML files with predefined extensions.
- Extracts dependencies based on configurable XML elements and attributes.
- Categorizes dependencies into MDS, HTTP, FILE, LOCAL, CUSTOM, and OTHER.
- Outputs categorized dependencies into CSV files.
- Allows custom filters to include specific dependencies.

## Prerequisites

- Python 3.8+
- `lxml` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sca-dependencies-finder.git
   cd sca-dependencies-finder
   ```
2. Install dependencies:
   ```bash
   pip install lxml
   ```

## Usage

Run the script with:

```bash
python main.py
```

By default, the script scans a predefined root directory (`sca_root_path`) set in `main.py`. Modify this path to match your target directory before running the script.

## Configuration

Modify `config.py` to customize:

- **File extensions** (`FILE_EXTENSIONS`): Defines which XML-based files are scanned.
- **Elements** (`ELEMENTS`): XML elements of interest.
- **Attributes** (`ATTRIBUTES`): XML attributes to extract dependencies from.
- **Ignored dependencies** (`IGNORES`): Tuple of (file extension, element, attribute) to exclude.

## Output

The script generates CSV files in the script's directory, one per dependency category:

- `MDS_dependencies.csv`
- `HTTP_dependencies.csv`
- `FILE_dependencies.csv`
- `LOCAL_dependencies.csv`
- `CUSTOM_dependencies.csv`
- `OTHER_dependencies.csv`

Each CSV file contains:

- **File**: The relative path of the XML file.
- **Element**: The XML element that contains the dependency.
- **Attribute**: The XML attribute where the dependency is defined.
- **Path**: The extracted dependency value.

## Code Structure

- `main.py` - Main script.
- `app.py` - Processes directories, extracts dependencies, and generates results.
- `config.py` - Contains XML file types, elements, attributes, and ignore rules.
- `helper.py` - Utility functions for file handling, CSV export, and XPath generation.
- `model.py` - Defines data models for dependency extraction and categorization.

## Example Output

```
'MDS_dependencies.csv' is created with 10 MDS dependencies.
'HTTP_dependencies.csv' is created with 5 HTTP dependencies.
'FILE_dependencies.csv' is created with 3 FILE dependencies.
'LOCAL_dependencies.csv' is created with 2 LOCAL dependencies.
'CUSTOM_dependencies.csv' is created with 4 CUSTOM dependencies.
'OTHER_dependencies.csv' is created with 6 OTHER dependencies.
```

## License

This project is licensed under the MIT License.

## Author

Ünver Can Ünlü - [GitHub](https://github.com/unvercan)
