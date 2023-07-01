from jproperties import Properties

properties = Properties()


class OpensearchConfig:
    _config = None

    @staticmethod
    def get_config():
        if OpensearchConfig._config is None:
            with open('properties/opensearch-client.properties', 'rb') as config_file:
                properties.load(config_file)
                _config = properties
                return _config
