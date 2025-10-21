import os, sys, yaml, __main__, shutil


class Config(dict):

    def __init__(self, conf=None):
        self.config = None
        default = os.path.abspath(os.path.join(os.path.dirname(__file__), "default.yaml"))
        local = os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), "config.yaml"))
        try:
            with open(default) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if data is not None:
                    dict.__init__(self, data)
            if not os.path.isfile(local):
                with open(local, 'w') as f:
                    pass
            with open(local) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if data is not None:
                    for key, value in data.items():
                        self[key] = value
        except Exception as e:
            print(f"Config syntax error ({e})")

    def __missing__(self, key):
        raise ConfigError(key)


class ConfigError(Exception):

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return repr(f"No {self.key} found in config")


config = Config()
