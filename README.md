# SCA Dependencies Finder

## Overview

SCA Dependencies Finder is a tool designed to extract and categorize XML-based dependencies from Oracle SOA Composite applications. It scans specified directories for XML files, extracts dependency
information, and outputs the results into categorized CSV files.

## Features

- Parses XML files to find dependencies based on elements and attributes.
- Categorizes dependencies into different types:
    - **MDS Dependencies** (`oramds:/` references)
    - **HTTP Dependencies** (`http:/` and `https:/` references)
    - **File Dependencies** (`file:/` references)
    - **Local Dependencies** (existing paths within the project)
    - **Custom Dependencies** (user-defined filters)
- Saves dependency results as CSV files.

## File Structure

```
sca-dependencies-finder/
│-- dependencies_result.py      # Handles categorized dependency results
│-- dependency.py               # Defines the Dependency model
│-- helper.py                   # Helper functions for CSV export and file existence check
│-- sca_dependencies_finder.py  # Main script to find and process dependencies
│-- README.md                   # Project documentation
```

## Installation

### Prerequisites

- Python 3.x
- `lxml` library (for XML parsing)

To install dependencies, run:

```bash
pip install lxml
```

## Usage

Run the script using:

```bash
python sca_dependencies_finder.py
```

This will:

1. Scan the `root` directory for XML-based dependencies.
2. Categorize dependencies into different types.
3. Generate CSV reports for each category.

### Output

The script will generate CSV files in the same directory as the script, including:

- `mds_dependencies.csv`
- `http_dependencies.csv`
- `file_dependencies.csv`
- `local_dependencies.csv`
- `all_dependencies.csv`
- `custom_dependencies.csv` (if custom filters are provided)

## Configuration

### Custom Dependency Filters

To define custom dependency filters, modify the `custom_filters` list in `sca_dependencies_finder.py`:

```python
custom_filters = [
    "custom_value_1",
    "custom_value_2"
]
```

These filters allow the script to categorize additional dependencies based on specific path patterns.
