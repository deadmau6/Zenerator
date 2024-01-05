from .director import Director
from .builder import DefaultConfigBuilder
from .map import ConfigurationMap
from ..utils import Utils
from pprint import pprint

class ConfigurationManager:
    """
    This tool manages both local and global configuration files.
    """

    def __init__(self, local_path=None, project=None, use_project_config=True, cmd_args={}):
        # Set up builder and Director
        builder = DefaultConfigBuilder()
        self._director = Director(builder)
        # Given parameters
        self.project = project
        self.use_project_config = use_project_config
        self.cmd_args = cmd_args
        # Path variables - config locations
        self.local_path = local_path
        self._global_path = self._director.builder.global_path
        self._project_path = None
        # Private
        self._config_map = None
        self._project_config = None
        self._global_config = None
        self._local_config = None

    @property
    def configuration(self):
        if self._config_map is None:
            default_config = self._director.build_config_with_args(
                local_path=self.local_path,
                project=self.project,
                use_project_config=self.use_project_config,
                kwargs=self.cmd_args)
            #
            self._config_map = ConfigurationMap(default_config)
        return self._config_map

    def load_global(self):
        if self._global_config is None:
            self._global_config = self._director.build_global()
        return self._global_config

    def load_local(self):
        if self._local_config is None:
            self._local_config = self._director.build_local(self.local_path)
        return self._local_config

    def load_project(self):
        if self._project_config is None:
            # Load the global config
            self.load_global()
            # Get the project path
            self._project_path = self._director.builder.get_project_path(self.project)
            self._project_config = self._director.build_local(self._project_path)
        return self._project_config
	
    def _use_config(self, typ=""):
        if typ == "local":
            self.load_local()
            return self.local_path, self._local_config
        if typ == "project":
            self.load_project()
            return self._project_path, self._project_config
        self.load_global()
        return self._global_path, self._global_config

    def list_entry(self, key=None, config_type="global"):
        """
        Print a section from the config file, if no key is given then the entire config will be printed to console.
        """
        fpath, config = self._use_config(config_type.lower())
        print(f"Using config file at '{fpath}'.\n")
        obj = config
        if key is not None:
            obj = config.get(key)
        if obj is None:
            print(f"Could not find value for {key}, entry is null.")
            obj = config
        pprint(obj)
        print()

    def add_entry(self, keys, value=None, config_type="global"):
        """
        Add a new entry to a configuration file. If no value is given then a null entry is added.
        If entry is nested then add the proceding keys in the correct order to reach the nested object.
        """
        fpath, config = self._use_config(config_type.lower())
        obj = config
        for key in keys:
            if key not in obj:
                # reached the bottom
                obj[key] = value
            elif isinstance(obj[key], dict):
                # is a nested object
                obj = obj[key]
            else:
                raise Exception(f"Cannot add new entry ({key}) because it already exists. Try updating instead.")
        return config, fpath

    def remove_entry(self, keys, value=None, config_type="global"):
        """
        Delete an entry from the configuration file. This removes the key and value from config.
        If entry is nested then add the proceding keys in the correct order to reach the nested object.
        If the object is a list and the value is provided then the value will be deleted from the list.
        """
        fpath, config = self._use_config(config_type.lower())
        obj = config
        final = keys.pop(-1)
        for key in keys:
            if key in obj and isinstance(obj[key], dict):
                # is a nested object
                obj = obj[key]
            else:
                raise Exception(f"Entry ({key}) does not exists in {obj}.")
        #
        if final not in obj:
            raise Exception(f"Entry ({key}) does not exists in {obj}.")
        elif isinstance(obj[final], list) and value is not None:
            obj[final].remove(value)
        else:
            del obj[final]
        return config, fpath
    
    def update_entry(self, keys, value=None, config_type="global"):
        """
        Update an existing entry to a configuration file. If no value is given then the entry is updated to be null.
        If entry is nested then add the proceding keys in the correct order to reach the nested object.
        If the object is a list and the value is provided then the value will be appended the list.
        """
        fpath, config = self._use_config(config_type.lower())
        obj = config
        final = keys.pop(-1)
        for key in keys:
            if key in obj and isinstance(obj[key], dict):
                # is a nested object
                obj = obj[key]
            else:
                raise Exception(f"Entry ({key}) does not exists in {obj}.")
        #
        if final not in obj:
            raise Exception(f"Entry ({key}) does not exists in {obj}.")
        elif isinstance(obj[final], list) and value is not None:
            obj[final].append(value)
        else:
            obj[final] = value
        return config, fpath

    @staticmethod
    def save_config(config, fname):
        """Save the json file by writing it to disk."""
        Utils.write_to_json(config, fname)


    def start(self, args):
        """
        This method is used when running the manager as a standalone process from the command line.
        Typically this would be used to view or edit the configuration file.
        """
        self.local_path = args.local_path
        self.project = args.project
        config_type = "global"
        if args.local_path:
            config_type = "local"
        if args.project:
            config_type = "project"
        config, fpath = None, None
        if args.add:
            # TODO: cast values
            config, fpath = self.add_entry(keys=args.add, value=args.value, config_type=config_type)
        elif args.remove:
            config, fpath = self.remove_entry(keys=args.remove, config_type=config_type)
        elif args.update:
            config, fpath = self.update_entry(keys=args.update, value=args.value, config_type=config_type)
        if config is not None:
            print(f"Using config file at '{fpath}'.")
            if not args.dry_run:
                # TODO: validate before writing to disk
                ConfigurationManager.save_config(config, fpath)
            print("New Config:")
            pprint(config)
        else:
            self.list_entry(key=args.list, config_type=config_type)