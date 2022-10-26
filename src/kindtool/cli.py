import argparse

from kindtool import __app_name__, __version__, cmdinit, cmdup, cmddestroy, templates

def add_default_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument( '--directory', '-d', type=str,
        metavar='DIR',
        default='',
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
        default='',
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

def create_parser_status(parent: argparse.ArgumentParser) -> None:
    name = 'status'
    help = 'prints status information of the cluster'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_name(parent: argparse.ArgumentParser) -> None:
    name = 'name'
    help = 'name of the cluster'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_kubeconfig(parent: argparse.ArgumentParser) -> None:
    name = 'kubeconfig'
    help = 'returns the directory containing the kubeconfig of the cluster'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_ingress(parent: argparse.ArgumentParser) -> None:
    name = 'ingress'
    help = 'returns True or False if ingress feature was enabled'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def main() -> None:
    parser = main_parser()
    subparser = parser.add_subparsers(dest='command')
    create_parser_init(subparser)
    create_parser_up(subparser)
    create_parser_destroy(subparser)
    create_parser_status(subparser)

    # 'get' has subcommands
    parser_get = subparser.add_parser('get', help='get useful status information of the cluster')
    subparser = parser_get.add_subparsers(dest='get')

    create_parser_get_name(subparser)
    create_parser_get_kubeconfig(subparser)
    create_parser_get_ingress(subparser)

    args = parser.parse_args()

    if args.command == 'init':
        tpl = templates.Templates(dest_dir=args.directory)
        cmd = cmdinit.CmdInit(tpl)
        cmd.create_content()
    elif args.command == 'up':
        tpl = templates.Templates(dest_dir=args.directory)
        cmd = cmdup.CmdUp(tpl)
        cmd.run()
    elif args.command == 'destroy':
        tpl = templates.Templates(dest_dir=args.directory)
        cmd = cmddestroy.CmdDestroy(tpl)
        cmd.run(args.force)
    elif args.command == 'status':
        raise NotImplementedError(f"command '{args.command}' is not implemented")
    elif args.command == 'get':
        raise NotImplementedError(f"command '{args.command}' is not implemented")
        # if args.get == 'name':
        #     print(f'get {args.get} with {args.directory=}')
        # if args.get == 'kubeconfig':
        #     print(f'get {args.get} with {args.directory=}')
        # if args.get == 'ingress':
        #     print(f'get {args.get} with {args.directory=}')
        # else:
        #     parser_get.print_usage()
    else:
        parser.print_usage()