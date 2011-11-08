import base64
import urllib2
import urllib
import json

class NullAuth(object):
    @property
    def retriable(self):
        return False

    def authenticate(self, request):
        pass

class BasicAuth(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def retriable(self):
        return False

    def authenticate(self, request):
        user_pass = '{0}:{1}'.format(urllib2.quote(self.username), urllib2.quote(self.password))
        credentials = base64.b64encode(user_pass).strip()
        request.add_header('Authorization', 'Basic {0}'.format(credentials))

class OAuth2Auth(object):
    def __init__(self, access_token=None, refresh_token=None, scope=None,
                 client_id=None, client_secret=None, token_url=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._retry_count = 0

    @property
    def retriable(self):
        return self._retry_count < 1

    def authenticate(self, request):
        request.add_header('Authorization', 'Bearer {0}'.format(self.access_token))

    def prepare_retry(self):
        self._retry_count = self._retry_count + 1
        req = urllib2.Request(self.token_url)
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        req.add_data(urllib.urlencode(data))
        res = json.load(urllib2.urlopen(req))
        if res.get('access_token'):
            self.access_token = res['access_token']
            self.refresh_token = res['refresh_token']
            if hasattr(self, 'refresh_callback'):
                return self.refresh_callback(res)
        return
