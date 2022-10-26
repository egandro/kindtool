import argparse
from email.policy import default

from kindtool import __app_name__, __version__, cmdinit, cmdup, cmddestroy, templates

def add_default_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument( '--directory', '-d', type=str,
        metavar='DIR',
        help="directory of Kindfile (default is current working directory)", required=False)

def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=__app_name__)
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
    return parser

def create_parser_init(parent: argparse.ArgumentParser) -> None:
    name = 'init'
    help = 'create a new Kindfile'

    parser = parent.add_parser(name, help=help)
    parser.add_argument( '--directory', '-d', type=str,
        metavar='DIR',
        help="destination directory (default is current working directory)", required=False)

def create_parser_up(parent: argparse.ArgumentParser) -> None:
    name = 'up'
    help = 'start a cluster'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_destroy(parent: argparse.ArgumentParser) -> None:
    name = 'destroy'
    help = 'stops a cluster'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)
    parser.add_argument('--force','-f', action='store_true',
        help="force the deletion")


def main() -> None:

    parser = main_parser()
    subparser = parser.add_subparsers(dest='command')
    create_parser_init(subparser)
    create_parser_up(subparser)
    create_parser_destroy(subparser)

    args = parser.parse_args()

    if args.command == 'init':
        print(f'init with {args.directory}')
    elif args.command == 'up':
        print(f'up with {args.directory}')
    elif args.command == 'destroy':
        print(f'destroy with {args.directory}, {args.force}')
    else:
        parser.print_usage()