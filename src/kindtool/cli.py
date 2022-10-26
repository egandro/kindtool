import argparse

from kindtool import __app_name__, __version__, cmdinit, cmdup, cmddestroy, templates

# # Create the parser
# parser = argparse.ArgumentParser(__app_name__)

# # Add an argument
# parser.add_argument('--name', type=str, required=False)


def main() -> None:
    parser = argparse.ArgumentParser(prog=__app_name__)
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    subparser = parser.add_subparsers(dest='command')

    login = subparser.add_parser('login', help='verbose output')
    login.add_argument('--username', type=str, required=True)
    login.add_argument('--password', type=str, required=True)

    register = subparser.add_parser('register')
    register.add_argument('--firstname', type=str, required=True)
    register.add_argument('--lastname', type=str, required=True)
    register.add_argument('--username', type=str, required=True)
    register.add_argument('--email', type=str, required=True)
    register.add_argument('--password', type=str, required=True)

    args = parser.parse_args()
    if args.command == 'login':
        print('Logging in with username:', args.username,'and password:', args.password)
    elif args.command == 'register':
        print('Creating username', args.username,'for new member', args.firstname, args.lastname,
            'with email:', args.email,
            'and password:', args.password)
    else:
        parser.print_usage()