import argparse

from kindtool import __app_name__, __version__, cmdinit, cmdget, cmdup, cmddestroy, cmddashboard, cmdshell, templates

def add_default_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument( '--directory', '-d', type=str,
        metavar='DIR',
        default='',
        help="directory of kindfile.yaml (default is current working directory)", required=False)

def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=__app_name__)
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
    return parser

def create_parser_init(parent: argparse.ArgumentParser) -> None:
    name = 'init'
    help = 'create a new kindfile.yaml'

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

def create_parser_dashboard(parent: argparse.ArgumentParser) -> None:
    name = 'dashboard'
    help = 'installs and start the k8s dashboard in the cluster'
    version = '2.6.1'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

    parser.add_argument( '--version', '-v', type=str,
        metavar='VER',
        default=version,
        help=f"version of the dashboard (default {version})", required=False)

def create_parser_shell(parent: argparse.ArgumentParser) -> None:
    name = 'shell'
    help = 'installs and start the k8s dashboard in the cluster'
    pod = 'shell-pod'
    image = 'ubuntu:22.04'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

    parser.add_argument( '--pod', '-p', type=str,
        metavar='POD',
        default=pod,
        help=f"name of the shell pod (default {pod})", required=False)
    parser.add_argument( '--image', '-i', type=str,
        metavar='IMAGE',
        default=image,
        help=f"docker image of the shell pod (default {image})", required=False)
    parser.add_argument( '--namespace', '-n', type=str,
        metavar='NS',
        default="default",
        help=f"name of the namespace", required=False)
    parser.add_argument( '--cmd', '-c', type=str,
        metavar='CMD',
        default="",
        help=f"command to run as shell (e.g. /bin/bash - default guesstimate shell)", required=False)
    parser.add_argument('--kill','-k', action='store_true',
        help="kill shell pod")


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
    help = 'returns True or False if ingress feature is enabled'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_ingress_http_port(parent: argparse.ArgumentParser) -> None:
    name = 'ingress_http_port'
    help = 'returns the ingress http port'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_ingress_https_port(parent: argparse.ArgumentParser) -> None:
    name = 'ingress_https_port'
    help = 'returns the ingress https port'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_metallb(parent: argparse.ArgumentParser) -> None:
    name = 'metallb'
    help = 'returns True or False if metallb feature is enabled'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_mountpoints(parent: argparse.ArgumentParser) -> None:
    name = 'mountpoints'
    help = 'returns True or False if the cluster has local persistant storage'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_api_server_address(parent: argparse.ArgumentParser) -> None:
    name = 'api_server_address'
    help = 'returns the ip address of the k8s API server'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def create_parser_get_internal_registry_prefix(parent: argparse.ArgumentParser) -> None:
    name = 'internal_registry_prefix'
    help = 'returns the prefix internal docker registry if internal_registry is enabled'

    parser = parent.add_parser(name, help=help)
    add_default_arguments(parser)

def main() -> None:
    parser = main_parser()
    subparser = parser.add_subparsers(dest='command')
    create_parser_init(subparser)
    create_parser_up(subparser)
    create_parser_destroy(subparser)
    create_parser_status(subparser)
    create_parser_dashboard(subparser)
    create_parser_shell(subparser)

    # 'get' has subcommands
    parser_get = subparser.add_parser('get', help='get useful status information of the cluster')
    subparser = parser_get.add_subparsers(dest='get')

    create_parser_get_name(subparser)
    create_parser_get_kubeconfig(subparser)
    create_parser_get_ingress(subparser)
    create_parser_get_ingress_http_port(subparser)
    create_parser_get_ingress_https_port(subparser)
    create_parser_get_metallb(subparser)
    create_parser_get_mountpoints(subparser)
    create_parser_get_api_server_address(subparser)
    create_parser_get_internal_registry_prefix(subparser)

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
    elif args.command == 'dashboard':
        tpl = templates.Templates(dest_dir=args.directory)
        cmd = cmddashboard.CmdDashboard(tpl, args.version)
        cmd.run()
    elif args.command == 'shell':
        tpl = templates.Templates(dest_dir=args.directory)
        cmd = cmdshell.CmdShell(tpl, args.pod, args.namespace, args.image, args.cmd)
        if args.kill:
            cmd.kill()
        else:
            cmd.create_or_attach()
    elif args.command == 'get':
        arr = [
            'name','kubeconfig',
            'ingress', 'ingress_http_port', 'ingress_https_port',
            'metallb',
            'mountpoints',
            'api_server_address',
            'internal_registry_prefix'
        ]
        if args.get in arr:
            tpl = templates.Templates(dest_dir=args.directory)
            cmd = cmdget.CmdGet(tpl)
            cmd.get(args.get)
        else:
            parser_get.print_usage()
    else:
        parser.print_usage()