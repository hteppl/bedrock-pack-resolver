from os import getenv


class Environment:
    _true = ["true", "yes", "y", "t", "1"]
    
    update_version = getenv("update_version", "False").lower() in _true
    create_glyphs_tables = getenv("create_glyphs_tables", "False").lower() in _true
