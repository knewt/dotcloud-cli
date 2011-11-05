import urllib2
import json

from .auth import BasicAuth, OAuth2Auth
from .response import *
from .errors import RESTAPIError, AuthenticationNotConfigured

class RESTClient(object):
    def __init__(self, endpoint='https://rest.dotcloud.com/1'):
        self.endpoint = endpoint
        self.authenticator = None

    def set_basic_auth(self, username, password):
        self.authenticator = BasicAuth(username, password)

    def set_oauth2_token(self, token):
        self.authenticator = OAuth2Auth(token)

    def build_url(self, path):
        if path.startswith('/'):
            return self.endpoint + path
        else:
            return path

    def get(self, path):
        url = self.build_url(path)
        req = urllib2.Request(url)
        return self.request(req)

    def post(self, path, payload={}):
        url = self.build_url(path)
        data = json.dumps(payload)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        return self.request(req)

    def put(self, path, payload={}):
        url = self.build_url(path)
        data = json.dumps(payload)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        req.get_method = lambda: 'PUT'
        return self.request(req)

    def delete(self, path):
        url = self.build_url(path)
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        return self.request(req)

    def patch(self, path, payload={}):
        url = self.build_url(path)
        data = json.dumps(payload)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        req.get_method = lambda: 'PATCH'
        return self.request(req)

    def request(self, req):
        if not self.authenticator:
            raise AuthenticationNotConfigured
        self.authenticator.authenticate(req)
        req.add_header('Accept', 'application/json')
        try:
            res = urllib2.urlopen(req)
            return self.make_response(res)
        except urllib2.HTTPError, e:
            raise RESTAPIError(code=e.code, desc=str(e))

    def make_response(self, res):
        if res.headers['Content-Type'] == 'application/json':
            data = json.loads(res.read())
        elif res.code == 204:
            return None
        else:
            raise RESTAPIError(code=500,
                               desc='Unsupported Media type: {0}'.format(res.headers['Content-Type']))
        if res.code >= 400:
            raise RESTAPIError(code=res.code, desc=data['description'])
        return BaseResponse.create(res=res, data=data)
