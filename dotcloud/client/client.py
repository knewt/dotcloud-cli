import urllib2
import json

from .wsse import apply_wsse_header
from .response import *

class RESTClient(object):
    def __init__(self, base_url='https://ws.dotcloud.com/1.0'):
        self.base_url = base_url

    def get(self, path):
        url = self.base_url + path
        req = urllib2.Request(url)
        apply_wsse_header(req)
        req.add_header('Accept', 'application/json')
        try:
            res = urllib2.urlopen(req)
            return self.make_response(res)
        except urllib2.HTTPError, e:
            return ErrorResponse(code=e.code, desc=e.message)

    def make_response(self, res):
        if res.headers['Content-Type'] == 'application/json':
            data = json.loads(res.read())
        else:
            return ErrorResponse(code=500,
                                 desc='Unsupported Media type: {0}'.format(res.headers['Content-Type']))
        if res.code >= 400:
            return ErrorReponse(code=res.code, desc=data['description'])
        return BaseResponse.create(res=res, data=data)
