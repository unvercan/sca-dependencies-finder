# XML file extensions
FILE_EXTENSIONS: list[str] = [
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
]

# XML elements
ELEMENTS: list[str] = [
    "reference",
    "component",
    "service",
    "import",
    "schemaImport",
    "schema-import",
    "schema"
]

# XML attributes
ATTRIBUTES: list[str] = [
    "location",
    "wsdlLocation",
    "schemaLocation",
    "localPart",
    "src"
]

# ignored file extension - element - attribute
IGNORES: list[tuple[str, str, str]] = [
    ("wsdl", "service", "location"),
]
