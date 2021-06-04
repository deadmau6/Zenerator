
class Director:
    """
    This Director is responsible for running the builders in order
    and then merge the objects into a single map(config_map).
    """
    def __init__(self, builder):
        self.builder = builder

    @property
    def builder(self):
        return self._builder
    
    @builder.setter
    def builder(self, b):
        self._builder = b

    def build_global(self):
        self._builder.reset()
        self._builder.build_global_config()
        return self._builder.config

    def build_local(self, local_path):
        self._builder.reset()
        self._builder.build_local_config(config=local_path, use_project_config=False)
        return self._builder.config

    def build_config_with_args(self, local_path=None, project=None, use_project_config=True, kwargs={}):
        self._builder.reset()
        # First build global
        self._builder.build_global_config()
        # Next build the local config
        if local_path is not None and project is not None:
            self._builder.build_local_config(config=local_path, project=project, use_project_config=use_project_config)
        # Finally build the user defined config
        if len(kwargs) >= 0:
            self._builder.build_usr_config(kwargs)
        return self._builder.config
