from .parser import get_parser
from ..client import RESTClient

import sys

class CLI(object):
    def __init__(self):
        self.client = RESTClient(base_url='https://ws.dotcloud.com/1.0')
    
    def run(self):
        p = get_parser()
        args = p.parse_args(args=sys.argv[1:])
        cmd = 'cmd_{0}'.format(args.cmd)
        if hasattr(self, cmd):
            getattr(self, cmd)(args)

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

        
