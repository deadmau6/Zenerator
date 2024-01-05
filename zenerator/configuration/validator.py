
class Validator:

    @classmethod
    def validate(cls, config, schema):
        """Validate the configuration dict with a schema."""
        norm_data = {}
        for key, value in schema.items():
            # TODO: custom validation errors
            if value.get('required', False) and key not in config:
                raise Exception(f"{key} is required")
            if key not in config:
                norm_data[key] = value.get('default')
            else:
                norm_data[key] = cls._validate_types(config[key], value)
        return norm_data

    @classmethod
    def _validate_types(cls, data, schema):
        # Check if nullable
        if schema.get('nullable', True) and data is None:
            return data
        typ = schema.get("type", "string")
        if typ == "dict":
            return cls._validate_dict(data, schema)
        if typ == "list":
            return cls._validate_list(data, schema)
        return cls._validate_basic_type(data, schema)

    @classmethod
    def _validate_basic_type(cls, data, schema):
        """For basic types like string, int, float, bool."""
        cast = schema.get("coerce")
        if cast is not None:
            data = cast(data)
        typ = schema.get("type", "string")
        if not cls._is_basic_type(data, typ):
            raise Exception(f"Expected type {typ} but instead got {type(data)}.")
        return data

    @classmethod
    def _is_basic_type(cls, value, typ):
        if typ == "integer":
            return isinstance(value, int)
        if typ == "float":
            return isinstance(value, float)
        if typ == "bool":
            return isinstance(value, bool)
        return isinstance(value, str)

    @classmethod
    def _validate_dict(cls, obj, kwargs):
        if len(obj) == 0:
            return kwargs.get('default')
        # TODO: obj_schema = kwargs.get('schema', {}) this is probably recursive.
        key_rules = kwargs.get('keysrules', {})
        value_rules = kwargs.get('valuesrules', {})
        norm_data = {}
        for key, value in obj.items():
            k = cls._validate_types(key, key_rules)
            v = cls._validate_types(value, value_rules)
            norm_data[k] = v
        return norm_data

    @classmethod
    def _validate_list(cls, obj, kwargs):
        if len(obj) == 0:
            return kwargs.get('default')
        # TODO: obj_schema = kwargs.get('schema', {}) this is probably recursive.
        schema = kwargs.get('schema', {})
        norm_data = []
        for value in obj:
            norm_data.append(cls._validate_types(value, schema))
        return norm_data