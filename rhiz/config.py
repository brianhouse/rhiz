import os, sys, yaml, __main__, shutil


class Config(dict):

    def __init__(self, conf=None):
        self.conf = None
        conf = os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), "config.yaml"))
        smp = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml.smp"))
        if not os.path.isfile(conf):
            shutil.copyfile(smp, conf)
        self.conf = conf
        f = open(self.conf)
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data is not None:
            dict.__init__(self, data)
        f.close()

    def __missing__(self, key):
        raise ConfigError(key, self.conf)


class ConfigError(Exception):

    def __init__(self, key, conf):
        self.key = key
        self.conf = conf

    def __str__(self):
        return repr("No '%s' in config (%s)" % (self.key, self.conf))


config = Config()
