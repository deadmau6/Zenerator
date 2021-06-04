from .configuration import ConfigurationManager
from pprint import pprint

class Core:

    def __init__(self):
        self._manager = ConfigurationManager()