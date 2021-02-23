import struct
import socket
import random
import sys
import re

from typing import List
from subprocess import Popen, PIPE
from os import path

from network.utils import is_valid_eth_address


def wake_up(eth_addr: str, bcasts: List[str] = ['192.168.0.255'], port: int = 0) -> None:
    ''' return a none

    eth_addr - device mac addres
    bcasts - list of broadcasts adrreses
    port - destination port

    sends the magic packet to broadcast address with device mac address which we want to power on remotely.

    In small local networks (with one router) it does not matter what port we set, because the packet will 
    always reach the destination (broadcast) that will send an ethernet frame addressed to the device
    that we want to start remotely (the option in the bios or in the graphics card device settings mustbe enabled). 
    In more extensive networks with more routers, the gateway must be properly configured to pass the 
    magic packet through, and here the port matters.
    '''
    if not is_valid_eth_address(eth_addr):
        raise ValueError("Incorrect entry, use 6-bytes physical address")

    address_oct: List[str] = eth_addr.split(
        ':') if eth_addr[2] == ':' else eth_addr.split('-')

    magic_packet: struct = struct.pack('!BBBBBB',
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


def status(ip_addres: str = None, eth_addr: str = None) -> bool:
    ''' return bool (true - online, false - offline)

    check the status of the device based on ip or mac address
    '''
    raise NotImplementedError