import socket


def is_valid_eth_address(eth_addr: str) -> bool:
    ''' return a bool

    eth_addr - mac address

    verification of the mac address independents of the operating system
    '''
    return True if len(eth_addr.split(':')) == 6 or len(eth_addr.split('-')) == 6 else False
