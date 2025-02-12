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
