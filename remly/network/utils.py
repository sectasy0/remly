import socket


def is_valid_eth_address(eth_addr: str) -> bool:
    ''' return a bool

    eth_addr - mac address

    verification of the mac address independents of the operating system
    '''
    return True if len(eth_addr.split(':')) == 6 or len(eth_addr.split('-')) == 6 else False



def is_valid_ipv4_address(ipv4_addr: str) -> bool:
    '''return a bool

    eth_addr - mac address

    verification of the ipv4 address
    '''
    try:
        socket.inet_pton(socket.AF_INET, ipv4_addr)
    except AttributeError:
        try:
            socket.inet_aton(ipv4_addr)
        except socket.error:
            return False
        return ipv4_addr.count('.') == 3
    except socket.error:
        return False

    return True