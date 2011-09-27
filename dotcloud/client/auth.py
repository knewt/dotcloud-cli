import os
import base64
import json
from urllib2 import unquote

# TODO: remove this
CONFIG_DIR = os.path.expanduser('~/.dotcloud')
CONFIG_FILE = os.path.basename(os.environ.get('DOTCLOUD_CONFIG_FILE', 'dotcloud.conf'))
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)

def authenticate(request):
    config = json.load(file(CONFIG_PATH))
    access_key, secret = config['apikey'].split(':')
    user_pass = '{0}:{1}'.format(unquote(access_key), unquote(secret))
    credentials = base64.b64encode(user_pass).strip()
    request.add_header('Authorization', 'Basic {0}'.format(credentials))
