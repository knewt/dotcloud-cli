import os
import json

class GlobalConfig(object):
    def __init__(self):
        self.dir = os.path.expanduser('~/.dotcloud')
        self.file = os.path.basename(os.environ.get('DOTCLOUD_CONFIG_FILE', 'dotcloud.conf'))
        self.path = os.path.join(self.dir, self.file)
        if 'DOTCLOUD_CONFIG_FILE' in os.environ:
            self.key = self.path + '.key'
        else:
            self.key = os.path.join(self.dir, 'dotcloud.key')
        self.load()

    def load(self):
        try:
            self.data = json.load(file(self.path))
            self.loaded = True
        except IOError:
            self.loaded = False

    def get(self, *args):
        if not self.loaded:
            return None
        return self.data.get(*args)

