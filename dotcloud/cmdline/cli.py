from .parser import get_parser
from ..client import RESTClient
from ..client.errors import RESTAPIError

import sys

class CLI(object):
    def __init__(self, debug=False, api_url=None):
        args = {}
        if api_url:
            args['base_url'] = api_url
        self.client = RESTClient(**args)
        self.debug = debug
        self.error_handlers = {
            401: self.error_authen,
            403: self.error_authz,
        }

    def run(self):
        p = get_parser()
        args = p.parse_args(args=sys.argv[1:])
        cmd = 'cmd_{0}'.format(args.cmd)
        if hasattr(self, cmd):
            try:
                getattr(self, cmd)(args)
            except RESTAPIError, e:
                handler = self.error_handlers.get(e.code, self.default_error_handler)
                handler(e)

    def default_error_handler(self, e):
        print >>sys.stderr, "Unhandled exception: {0}".format(e)

    def error_authen(self, e):
        print >>sys.stderr, "Authentication Error: {0}".format(e.code)

    def error_authz(self, e):
        print >>sys.stderr, "Authorization Error: {0}".format(e.desc)

    def cmd_list(self, args):
        res = self.client.get('/me/applications')
        for app in sorted(res):
            print app['name']

    def cmd_info(self, args):
        if args.environment is None:
            args.environment = 'default'
        url = '/me/applications/{0}/environments/{1}/services'.format(args.application, args.environment)
        res = self.client.get(url)
        for service in res:
            print '{0} (instances: {1})'.format(service['name'], len(service['instances']))

        
