import os
from abc import ABC, abstractmethod, abstractproperty
from ..utils import Utils
from ..constants import Constants
from .validator import Validator
from .schema import GLOBAL, LOCAL, CMDS

class Builder(ABC):
    """This is the configuration builder interface."""
    @abstractproperty
    def config(self):
        pass

    @abstractmethod
    def build_global_config(self, **kwargs):
        """Construct the configuration from the global config file."""
        raise NotImplementedError()

    @abstractmethod
    def build_local_config(self, **kwargs):
        """Construct the configuration from a local config file."""
        raise NotImplementedError()

    @abstractmethod
    def build_usr_config(self, **kwargs):
        """Construct the configuration from command line arguments and environment variables."""
        raise NotImplementedError()

class DefaultConfigBuilder(Builder):
    """Construct the configuration from command line arguments and environment variables."""
    GLOBAL_CONFIG_NAME = Constants.GLOBAL_CONFIG_NAME
    LOCAL_CONFIG_NAME = Constants.LOCAL_CONFIG_NAME
    ZENPATH_ENV_NAME = Constants.ZENPATH_ENV_NAME

    def __init__(self):
        # TODO: if config file does not exist then create it.
        # Get Global Config File Path
        self._global_config_path = None
        if os.getenv(self.ZENPATH_ENV_NAME):
            self._global_config_path = os.path.join(os.getenv(self.ZENPATH_ENV_NAME), self.GLOBAL_CONFIG_NAME)
        # Set the config object
        self.reset()

    def reset(self):
        self._config = {}

    @property
    def global_path(self):
        return self._global_config_path

    @property
    def config(self):
        return self._config

    def get_project_path(self, project):
        """Get the project path. Assumes that the global is loaded."""
        project_path = self._config.get('projects', {}).get(project)
        if project_path is None:
            raise Exception(f"Could not build local config: Project name - {project}, does not have config location.")
        return project_path

    def build_global_config(self, **kwargs):
        """Construct the configuration from the global config file."""
        fpath = self._global_config_path
        config = Utils.load_from_json(fpath)
        # See if another global config is set.
        other_config = config.get("useConfig", None)
        if other_config and os.path.exists(other_config):
            config = Utils.load_from_json(other_config)
        # Validate and normalize the configuration data.
        normal_config = Validator().validate(config, GLOBAL)
        self._config.update(normal_config)

    def build_local_config(self, **kwargs):
        """Construct the configuration from a local config file."""
        local_path = kwargs.get("config")
        project_name = kwargs.get("project")
        if local_path is None and project_name is None:
            raise Exception(f"Could not build local config: No path({local_path}) or project({project_name}) provided.")
        #
        v = Validator()
        use_project_config = kwargs.get("use_project_config", True)
        #
        if local_path is not None and os.path.exists(local_path):
            config = Utils.load_from_json(local_path)
            norm = v.validate(config, LOCAL)
            self._config.update(norm)
        #
        if use_project_config and project_name is not None:
            project_path = self.get_project_path(project_name)
            config = Utils.load_from_json(project_path)
            norm = v.validate(config, LOCAL)
            self._config.update(norm)

    def build_usr_config(self, **kwargs):
        """Construct the configuration from command line arguments and environment variables."""
        normal_config = v.validate(kwargs, CMDS)
        self._config.update(normal_config)