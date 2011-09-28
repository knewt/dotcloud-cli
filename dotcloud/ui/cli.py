from .parser import get_parser
from .version import VERSION
from ..client import RESTClient
from ..client.errors import RESTAPIError

import sys, os
import json
import subprocess
import re

# FIXME
CONFIG_DIR = os.path.expanduser('~/.dotcloud')
CONFIG_FILE = os.path.basename(os.environ.get('DOTCLOUD_CONFIG_FILE', 'dotcloud.conf'))
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
if 'DOTCLOUD_CONFIG_FILE' in os.environ:
    CONFIG_KEY = CONFIG_PATH + '.key'
else:
    CONFIG_KEY = os.path.join(CONFIG_DIR, 'dotcloud.key')

class CLI(object):
    __version__ = VERSION
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
        self.load_config(args)
        cmd = 'cmd_{0}'.format(args.cmd)
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
        print >>sys.stderr, message

    def default_error_handler(self, e):
        self.die("Unhandled exception: {0}".format(e))

    def error_authen(self, e):
        self.die("Authentication Error: {0}".format(e.code))

    def error_authz(self, e):
        self.die("Authorization Error: {0}".format(e.desc))

    def cmd_version(self, args):
        print 'dotcloud/' + self.__version__

    def cmd_list(self, args):
        res = self.client.get('/me/applications')
        for app in sorted(res.items):
            print app['name']

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

    @app_local
    def cmd_app(self, args):
        print args.application

    @app_local
    def cmd_env(self, args):
        print args.environment

    @app_local
    def cmd_info(self, args):
        url = '/me/applications/{0}/environments/{1}/services'.format(args.application, args.environment)
        res = self.client.get(url)
        for service in res.items:
            print '{0} (instances: {1})'.format(service['name'], len(service['instances']))
            self.dump_service(service['instances'][0], indent=2)

    def dump_service(self, instance, indent=0):
        def show(string):
            buf = ' ' * indent
            print buf + string
        show('runtime_config:')
        for (k, v) in instance['config'].iteritems():
            show('  {0}: {1}'.format(k, v))
        show('build_config:')
        for (k, v) in instance['build_config'].iteritems():
            show('  {0}: {1}'.format(k, v))
        show('URLs:')
        for port in instance['ports']:
            show('  {0}: {1}'.format(port['name'], port['url']))

    @app_local
    def cmd_url(self, args):
        type = 'http'
        url = '/me/applications/{0}/environments/{1}/services'.format(args.application, args.environment)
        res = self.client.get(url)
        for service in res.items:
            instance = service['instances'][0]
            u = [p for p in instance.get('ports', []) if p['name'] == type]
            if len(u) > 0:
                print '{0}: {1}'.format(service['name'], u[0]['url'])

    @app_local
    def cmd_ssh(self, args):
        # TODO support www.1
        url = '/me/applications/{0}/environments/{1}/services/{2}'.format(args.application, args.environment, args.service)
        res = self.client.get(url)
        for service in res.items:
            ports = service['instances'][0].get('ports', [])
            u = [p for p in ports if p['name'] == 'ssh']
            if len(u) > 0:
                self.run_ssh(u[0]['url'], '$SHELL').wait()

    @app_local
    def cmd_run(self, args):
        # TODO refactor with cmd_ssh
        url = '/me/applications/{0}/environments/{1}/services/{2}'.format(args.application, args.environment, args.service)
        res = self.client.get(url)
        for service in res.items:
            ports = service['instances'][0].get('ports', [])
            u = [p for p in ports if p['name'] == 'ssh']
            if len(u) > 0:
                self.run_ssh(u[0]['url'], ' '.join(args.command)).wait()

    def run_ssh(self, url, cmd, **kwargs):
        self.info('Connecting to {0}'.format(url))
        res = self.parse_url(url)
        options = (
            'ssh', '-t',
            '-i', CONFIG_KEY,
            '-o', 'LogLevel=QUIET',
            '-o', 'UserKnownHostsFile=/dev/null',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'PasswordAuthentication=no',
            '-o', 'ServerAliveInterval=10',
            '-l', res.get('user', 'dotcloud'),
            '-p', res.get('port'),
            res.get('host'),
            cmd
        )
        return subprocess.Popen(options, **kwargs)

    def parse_url(self, url):
        m = re.match('^(?P<scheme>[^:]+)://((?P<user>[^@]+)@)?(?P<host>[^:/]+)(:(?P<port>\d+))?(?P<path>/.*)?$', url)
        if not m:
            raise ValueError('"{url}" is not a valid url'.format(url=url))
        ret = m.groupdict()
        return ret
