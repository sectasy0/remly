import struct
import socket
import random
import sys
import re

from typing import List
from subprocess import Popen, PIPE
from os import path

from network.utils import (is_valid_eth_address,
                           is_valid_ipv4_address, crc16)
from network.arp import read_arptable


def wake_up(eth_addr: str, bcasts: List[str] = ['192.168.0.255'], port: int = 0) -> None:
    ''' return a none

    eth_addr - device mac addres
    bcasts - list of broadcasts adrreses
    port - destination port

    sends the magic packet to broadcast address with device mac address which we want to power on remotely.

    In small local networks (with one router) it does not matter what port we set, because the packet will 
    always reach the destination (broadcast) that will send an ethernet frame addressed to the device
    that we want to start remotely (the option in the bios or in the network card device settings mustbe enabled). 
    In more extensive networks with more routers, the gateway must be properly configured to pass the 
    magic packet through, and here the port matters.
    '''
    if not is_valid_eth_address(eth_addr):
        raise ValueError("Incorrect entry, use 6-bytes physical address")

    address_oct: List[str] = eth_addr.split(
        ':') if eth_addr[2] == ':' else eth_addr.split('-')

    magic_packet: bytes = struct.pack('!BBBBBB',
                                       int(address_oct[0], 16),
                                       int(address_oct[1], 16),
                                       int(address_oct[2], 16),
                                       int(address_oct[3], 16),
                                       int(address_oct[4], 16),
                                       int(address_oct[5], 16),
                                       )

    magic_packet = b'\xff' * 6 + magic_packet * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        for bcast in bcasts:
            sock.sendto(magic_packet, (bcast, port))
        sock.close()



def status(ip_address: str = None, eth_addr: str = None, port: int = 1, timeout: int = 1) -> bool:
    ''' return bool (true - online, false - offline)

    check the status of the device based on ip or mac address
    '''
    if eth_addr:
        ip_address = read_arptable(eth_addr)

    if is_valid_ipv4_address(ip_address):
        ICMP_ECHO_REQUEST: int = 8
        ICMP_CODE: int = socket.getprotobyname('icmp')

        ident: int = int((id(1) * random.random()) % 65535)
        icmp_header: bytes = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, int(
            ident), 1)

        payload: bytes = bytes((16 * 'Q').encode())
        
        packet_checksum: int = int(crc16(icmp_header + payload))
        icmp_header = struct.pack(
            '!BBHHH', ICMP_ECHO_REQUEST, 0, packet_checksum, ident, 1)

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE) as __sock:
            try:
                __sock.settimeout(timeout)
                __sock.sendto(icmp_header+payload, (ip_address, port))
                raw_data: bytes = __sock.recv(1024)
                icmp_header: tuple = struct.unpack('!BBHHH', raw_data[20:28])
                if icmp_header[0] == 0:
                    return True
            except socket.timeout:
                return False

            __sock.close()
    else:
        raise ValueError('Incorrect entry, please use IPv4 CIDR or mac format')
    