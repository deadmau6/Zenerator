from os import path
import json

class Utils:
	
    @staticmethod
    def load_from_json(fpath):
        """Load a valid json configuration file and return a dictionary."""
        root, ext = path.splitext(fpath)
        if ext.lower() == '.json':
            data = {}
            with open(fpath, 'r') as f:
                data = json.load(f)
            return data
        else:
            raise Exception(f"Invalid file, was expecting json but got {ext}")

    @staticmethod
    def write_to_json(data, fpath):
        """Load a valid json configuration file and return a dictionary."""
        root, ext = path.splitext(fpath)
        if ext.lower() == '.json':
            with open(fpath, "w+") as f:
                json.dump(data, f, indent=4)
        else:
            raise Exception(f"Invalid file, was expecting json but got {ext}")