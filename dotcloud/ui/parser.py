import argparse

def _init_parser():
    parser = argparse.ArgumentParser(prog='dotcloud', description='dotcloud CLI')
    parser.add_argument('--application', '-A', help='specify the application')
    parser.add_argument('--environment', '-E', help='specify the environment')
    
    subcmd = parser.add_subparsers(dest='cmd')

    subcmd.add_parser('list', help='list applications')
    subcmd.add_parser('info', help='Get information about the application')

    conn = subcmd.add_parser('connect', help='Connect a local directory with an existing app')
    conn.add_argument('application', help='specify the application')

    return parser

_p = _init_parser()

def get_parser():
    return _p
    


