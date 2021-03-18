from remly import wake_up, status

import argparse

def cli() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Cli script allow turn on your computer remotely and check status")
    subparsers = parser.add_subparsers(help='commands', dest='command')

    parser_status = subparsers.add_parser('s', help='check device status (accept ipv4 and mac)')
    parser_status.add_argument('--mac', '-m', dest='eth_addr', type=str, help='device physical address', required=False, default=argparse.SUPPRESS)
    parser_status.add_argument('--ipv4', '-v4', dest='ip_address', type=str, help='device ipv4 address', required=False, default=argparse.SUPPRESS)
    parser_status.add_argument('--port', '-p', dest='port', type=int, help='port for ICMP protocol (default: 7)', required=False, default=argparse.SUPPRESS)
    parser_status.add_argument('--timeout', '-t', dest='timeout', type=int, help='', required=False, default=argparse.SUPPRESS)

    parser_wake = subparsers.add_parser('w', help="wake up computer")
    parser_wake.add_argument('--mac', '-m', dest='eth_addr', type=str, help='device physical address', required=False, default=argparse.SUPPRESS)
    parser_wake.add_argument('--port', '-p', dest='port', type=int, help='port for WoL protocol (default: 9)', required=False, default=argparse.SUPPRESS)
    parser_wake.add_argument('--bcasts','-b', dest='bcasts', type=str, help='broadcast address (default: 192.168.0.255)', required=False, default=argparse.SUPPRESS, nargs='+')

    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.print_usage()
        return

    if args['command'] == 's':
        del args['command']
        if not args:
            parser_status.print_usage()
            return
        status(**args)
    elif args['command'] == 'w':
        del args['command']
        if not args:
            parser_wake.print_usage()
            return
        wake_up(**args)