import argparse

def _init_parser():
    parser = argparse.ArgumentParser(prog='dotcloud', description='dotcloud CLI')
    parser.add_argument('--application', '-A', help='specify the application')
    parser.add_argument('--environment', '-E', help='specify the environment')
    
    subcmd = parser.add_subparsers(dest='cmd')

    subcmd.add_parser('list', help='list applications')

    conn = subcmd.add_parser('connect', help='Connect a local directory with an existing app')
    conn.add_argument('application', help='specify the application')

    info = subcmd.add_parser('info', help='Get information about the application')
    info.add_argument('service', nargs='?', help='Specify the service')

    url = subcmd.add_parser('url', help='Show URL for the application')
    url.add_argument('service', nargs='?', help='Specify the service')

    ssh = subcmd.add_parser('ssh', help='SSH into the service')
    ssh.add_argument('service', help='Specify the service')

    run = subcmd.add_parser('run', help='SSH into the service')
    run.add_argument('service', help='Specify the service')
    run.add_argument('command', nargs='+', help='Run a command on the service')

    return parser

_p = _init_parser()

def get_parser():
    return _p
    


