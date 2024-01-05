import pytest
from zenerator.configuration import ConfigurationManager, ConfigurationMap

class TestConfiguration:

    def test_config_map(self):
        temp = { "a": 1, "b": 2, "c": 3 }
        temp_map = ConfigurationMap(temp)
        assert temp_map["a"] == 1
        assert temp_map.get("b") == 2
        assert temp_map.get("d", 0) == 0
        assert len(temp_map) == 3
        with pytest.raises(TypeError) as exc:
            temp_map["c"] = 4
        assert "object does not support item assignment" in str(exc.value)