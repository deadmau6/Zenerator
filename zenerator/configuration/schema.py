"""
Configuration Schemas.
This modeled after the python cerberus package, but we currently do not explicitly use it
in order to prevent users from having to download dependencies.

"""
EMPTY_DICT_STRINGS = {
    "type": "dict",
    "keysrules": {"type": "string"},
    "valuesrules": {"type": "string"},
    "default": {}
}

GLOBAL = {
    "useConfig": { "type": "string" },
    "projects": { **EMPTY_DICT_STRINGS, 'required': True },
}

LOCAL = {
    "operations": { "type": "list", "schema": {"type": "string"}},
    "arguments": { **EMPTY_DICT_STRINGS },
    "templates": { **EMPTY_DICT_STRINGS }
}

CMDS = {}