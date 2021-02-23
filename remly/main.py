from remly.remly import wake_up

import argparse

def cli() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Turn on your computer remotely")
    parser.add_argument('-m', dest="eth_addr", type=str,
                        help="device ethernet address", required=True)
    parser.add_argument('-p', dest="port", type=int, help="port for WoL protocol (default: 9)",
                        required=False, default=argparse.SUPPRESS)
    parser.add_argument('-b', dest="bcasts", type=str, help="broadcast address (default: 192.168.0.255)",
                        required=False, default=argparse.SUPPRESS, nargs="+")

    wake_up(**vars(parser.parse_args()))