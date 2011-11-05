import base64
from urllib2 import unquote

class NullAuth(object):
    def authenticate(self, request):
        pass

class BasicAuth(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, request):
        user_pass = '{0}:{1}'.format(quote(self.username), quote(self.password))
        credentials = base64.b64encode(user_pass).strip()
        request.add_header('Authorization', 'Basic {0}'.format(credentials))

class OAuth2Auth(object):
    def __init__(self, token):
        self.token = token

    def authenticate(self, request):
        request.add_header('Authorization', 'Bearer {0}'.format(self.token))
