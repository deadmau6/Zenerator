from collections.abc import Mapping

class ConfigurationMap(Mapping):
    """This is the read only configuration dictionary"""
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
