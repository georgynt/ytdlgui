import yaml

from os.path import exists
from core.singleton import Singleton


default_config_object = {
    'windows': {
        "main"    : {
            "left" : 0, "top": 0,
            "width": 500, "height": 400},
        "settings": {
            "left" : 0, "top": 0,
            "width": 500, "height": 400},
    },
    'settings': {
        'proxy': None,
        'parallel': 5
    }
}


class Config(dict, metaclass=Singleton):
    FILENAME = 'ytdl.conf'

    def __init__(self):
        self.__fname = self.FILENAME
        if not exists(self.__fname):
            super().__init__(default_config_object)
            self.save()
        else:
            with open(self.__fname, 'r') as f:
                self.update(yaml.load(f, yaml.SafeLoader))

    def save(self):
        if len(self):
            with open(self.__fname, 'w') as f:
                yaml.dump(dict(self), f, )

    @property
    def windows(self) -> dict:
        if 'windows' not in self:
            self['windows'] = {}
        return self['windows']

    @property
    def settings(self) -> dict:
        if 'settings' not in self:
            self['settings'] = {}
        return self['settings']
