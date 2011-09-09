from .parser import get_parser
from ..client import RESTClient
from ..client.errors import RESTAPIError

import sys, os
import json

class CLI(object):
    __version__ = '2.0.0'
    def __init__(self, debug=False, endpoint=None):
        self.client = RESTClient(endpoint=endpoint)
        self.debug = debug
        self.error_handlers = {
            401: self.error_authen,
            403: self.error_authz,
        }

    def run(self):
        p = get_parser()
        args = p.parse_args(args=sys.argv[1:])
        cmd = 'cmd_{0}'.format(args.cmd)
        self.load_config(args)
        if hasattr(self, cmd):
            try:
                getattr(self, cmd)(args)
            except RESTAPIError, e:
                handler = self.error_handlers.get(e.code, self.default_error_handler)
                handler(e)

    def app_local(func):
        def wrapped(self, args):
            if args.application is None:
                self.die('DotCloud application is not connected. '
                         'Run `dotcloud create <appname>` or `dotcloud connect <appname>`')
            if args.environment is None:
                args.environment = 'default'
            func(self, args)
        return wrapped

    def save_config(self, config):
        dir = '.dotcloud'
        if not os.path.exists(dir):
            os.mkdir(dir, 0700)
        f = open(os.path.join(dir, 'config'), 'w+')
        json.dump(config, f)

    def load_config(self, args):
        try:
            io = open('.dotcloud/config')
            config = json.load(io)
            if not args.application:
                args.application = config['application']
            if not args.environment:
                args.environment = config['environment']
        except IOError, e:
            pass

    def die(self, message):
        print >>sys.stderr, message
        sys.exit(1)

    def info(self, message):
        print message

    def default_error_handler(self, e):
        self.die("Unhandled exception: {0}".format(e))

    def error_authen(self, e):
        self.die("Authentication Error: {0}".format(e.code))

    def error_authz(self, e):
        self.die("Authorization Error: {0}".format(e.desc))

    def cmd_list(self, args):
        res = self.client.get('/me/applications')
        for app in sorted(res):
            print app['name']

    @app_local
    def cmd_info(self, args):
        url = '/me/applications/{0}/environments/{1}/services'.format(args.application, args.environment)
        res = self.client.get(url)
        for service in res:
            print '{0} (instances: {1})'.format(service['name'], len(service['instances']))

    def cmd_connect(self, args):
        url = '/me/applications/{0}'.format(args.application)
        try:
            res = self.client.get(url)
            self.info('Connecting with the application "{0}"'.format(args.application))
            self.save_config({
                'application': args.application,
                'environment': 'default',
                'version': self.__version__
            })
        except RESTAPIError:
            self.die('Application "{0}" doesn\'t exist. Try `dotcloud create <appname>`.'.format(args.application))
