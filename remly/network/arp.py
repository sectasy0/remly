from subprocess import Popen, PIPE
from os import path
import re, sys
import struct, socket

def read_arptable(eth_addr: str = None, ipv4_addr: str = None) -> str:
    ''' return a string

    eth_addr - mac address

    universal way to get ip address and mac from the system ARP table
    select one of the parameters, eth_addr has priority if you fill up both
    '''
    searchstr: str = None
    addr_type: int = 0 #    0 - mac address    1 - ipv4 address

    if eth_addr and isinstance(eth_addr, str):
        searchstr = eth_addr.replace(
            ':', '.?') if eth_addr[2] == ':' else eth_addr.replace('-', '.?')
    elif ipv4_addr and isinstance(ipv4_addr, str):
        addr_type = 1
        searchstr = ipv4_addr.replace('.', '.?')
    else: raise ValueError('ipv4 addres and mac addres must be a string')
    
    try:
        output = Popen(['arp', '-a'], stdout=PIPE,
                       stderr=PIPE).communicate()[0].decode('utf-8')
        for line in output.strip().split('\n'):
            if re.search(searchstr, line, re.IGNORECASE):
                return line.split()[addr_type]
    except FileNotFoundError:
        arp_cache: str = '/proc/net/arp'
        if path.exists(arp_cache):
            with open(arp_cache, 'r') as file:
                for line in file.readlines()[1:]:
                    line = line.strip()
                    if re.search(searchstr, line):
                        # for posix systems in this case addr_type for ipv4 must be addr_type + 2
                        # see /proc/net/arp 
                        return line.split()[addr_type] if addr_type == 0 else line.split()[addr_type + 2]
        else:
            return None