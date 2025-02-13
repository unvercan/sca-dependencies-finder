from pathlib import Path

# XML file extensions
FILE_EXTENSIONS: frozenset[str] = frozenset({
    "wsdl",
    "xsd",
    "xml",
    "xsl",
    "bpel",
    "componentType",
    "decs",
    "dvm",
    "jpr",
    "edl",
    "jca",
    "jws",
    "config",
    "monitor",
    "mwp",
    "rules",
    "sch",
    "schema",
    "table",
    "offlinedb"
})

# XML elements
ELEMENTS: frozenset[str] = frozenset({
    "reference",
    "component",
    "service",
    "import",
    "schemaImport",
    "schema-import",
    "schema"
})

# XML attributes
ATTRIBUTES: frozenset[str] = frozenset({
    "location",
    "wsdlLocation",
    "schemaLocation",
    "localPart",
    "src"
})

# ignored file extension - element - attribute
IGNORES: frozenset[tuple[str, str, str]] = frozenset({
    ("wsdl", "service", "location"),
})

# MDS dependency filters
MDS_FILTERS: frozenset[str] = frozenset({
    "oramds:/"
})

# HTTP dependency filters
HTTP_FILTERS: frozenset[str] = frozenset({
    "http:/",
    "https:/"
})

# FILE dependency filters
FILE_FILTERS: frozenset[str] = frozenset({
    "file:/"
})

# default values
DEFAULT = {
    "input": Path.cwd(),
    "output": Path.cwd(),
    "format": "csv",
    "prefix": "dependencies",
    "datetime_format": "%Y%m%d_%H%M%S",
    "logging_format": "%(asctime)s - %(levelname)s - %(message)s",
    "delimiter": ",",
    "encoding": "utf-8"
}
