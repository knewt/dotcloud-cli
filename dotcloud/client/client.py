import urllib2
import json

from .auth import authenticate
from .response import *
from .errors import RESTAPIError

class RESTClient(object):
    def __init__(self, endpoint='https://ws.dotcloud.com/1.0'):
        self.endpoint = endpoint

    def get(self, path):
        url = self.endpoint + path
        req = urllib2.Request(url)
        authenticate(req)
        req.add_header('Accept', 'application/json')
        try:
            res = urllib2.urlopen(req)
            return self.make_response(res)
        except urllib2.HTTPError, e:
            raise RESTAPIError(code=e.code, desc=str(e))

    def make_response(self, res):
        if res.headers['Content-Type'] == 'application/json':
            data = json.loads(res.read())
        else:
            raise RESTAPIError(code=500,
                               desc='Unsupported Media type: {0}'.format(res.headers['Content-Type']))
        if res.code >= 400:
            raise RESTAPIError(code=res.code, desc=data['description'])
        return BaseResponse.create(res=res, data=data)
