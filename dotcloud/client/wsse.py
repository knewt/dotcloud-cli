import hashlib
import datetime
import os
import json
import base64
import time
import datetime
import random

# TODO: remove this
CONFIG_DIR = os.path.expanduser('~/.dotcloud')
CONFIG_FILE = os.path.basename(os.environ.get('DOTCLOUD_CONFIG_FILE', 'dotcloud.conf'))
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)

def generate_wsse_token():
    config = json.load(file(CONFIG_PATH))
    access_key, secret = config['apikey'].split(':')
    template = 'UsernameToken Username="%(username)s", ' \
        'PasswordDigest="%(password)s", ' \
        'Nonce="%(nonce)s", ' \
        'Created="%(created)s"'
    nonce = hashlib.sha1(str(time.time() + random.random())).digest()
    nonce_b64 = base64.encodestring(nonce).strip()
    created = datetime.datetime.utcnow().isoformat() + 'Z'
    vars = {
        'username': access_key,
        'nonce': nonce_b64,
        'created': created,
        'password': generate_password_digest(nonce, created, str(secret))
    }
    return template % vars

def generate_password_digest(nonce, created, password):
    digest = hashlib.sha1(nonce + created + password).digest()
    return base64.encodestring(digest).strip()

def apply_wsse_header(req):
    token = generate_wsse_token()
    req.add_header('Authorization', 'WSSE profile="UsernameToken"')
    req.add_header('X-WSSE', token + 'f')
