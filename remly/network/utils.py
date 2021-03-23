import socket
import struct

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
    if ipv4_addr is None: return False
    
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


def crc16(packet: bytes) -> bytes:
    '''return bytes

    packet - data to generate crc

    crc16 checksum algorith
    '''
    total: int = 0
    num_words: int = len(packet) // 2
    for chunk in struct.unpack("!%sH" % num_words, packet[0:num_words*2]):
        total += chunk

    if len(packet) % 2:
        total += ord(packet[-1]) << 8

    total = (total >> 16) + (total & 0xffff)
    total += total >> 16
    return (~total + 0x10000 & 0xffff)