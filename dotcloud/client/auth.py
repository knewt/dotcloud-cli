import base64
from urllib2 import unquote

class BasicAuth(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, request):
        user_pass = '{0}:{1}'.format(unquote(self.username), unquote(self.password))
        credentials = base64.b64encode(user_pass).strip()
        request.add_header('Authorization', 'Basic {0}'.format(credentials))
