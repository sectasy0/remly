from struct import pack, unpack
from random import random
import socket

from typing import List

from remly.network.utils import (is_valid_eth_address,
                           is_valid_ipv4_address, crc16)
from remly.network.arp import read_arptable


def wake_up(eth_addr: str, bcasts: List[str] = ['192.168.0.255'], port: int = 9) -> None:
    '''
    sends the magic packet to broadcast address with device mac address which we want to power on remotely.
    '''
    if not is_valid_eth_address(eth_addr):
        raise ValueError("Incorrect entry, use 6-bytes physical address")
    
    address_oct: List[str] = eth_addr.split(
        ':') if eth_addr[2] == ':' else eth_addr.split('-')

    magic_packet: bytes = pack('!BBBBBB',
                                int(address_oct[0], 16),
                                int(address_oct[1], 16),
                                int(address_oct[2], 16),
                                int(address_oct[3], 16),
                                int(address_oct[4], 16),
                                int(address_oct[5], 16),
                            )

    magic_packet = b'\xff' * 6 + magic_packet * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as __sock:
        __sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        for bcast in bcasts:
            __sock.sendto(magic_packet, (bcast, port))
        __sock.close()



def status(ip_address: str = None, eth_addr: str = None, port: int = 1, timeout: int = 1) -> bool:
    '''
    check the status of the device based on ip or mac address
    '''
    if eth_addr:
        ip_address = read_arptable(eth_addr)

    if is_valid_ipv4_address(ip_address):
        ICMP_ECHO_REQUEST: int = 8
        ICMP_CODE: int = socket.getprotobyname('icmp')

        ident: int = int((id(1) * random()) % 65535)
        icmp_header: bytes = pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, int(
            ident), 1)

        payload: bytes = bytes((16 * 'Q').encode())
        
        packet_checksum: int = int(crc16(icmp_header + payload))
        icmp_header = pack('!BBHHH', ICMP_ECHO_REQUEST, 0, packet_checksum, ident, 1)

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE) as __sock:
            try:
                __sock.settimeout(timeout)
                __sock.sendto(icmp_header+payload, (ip_address, port))
                raw_data: bytes = __sock.recv(1024)
                icmp_header: tuple = unpack('!BBHHH', raw_data[20:28])
                if icmp_header[0] == 0:
                    return True
            except socket.timeout:
                return False

            __sock.close()
    else:
        raise ValueError('Incorrect entry, please use IPv4 CIDR or mac format')
    
