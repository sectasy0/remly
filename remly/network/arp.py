from subprocess import Popen, PIPE
from os import path
import re, sys

def ipv4_arptable(eth_addr: str) -> str:
    ''' return a string

    eth_addr - mac address

    universal way to get ip address from the ARP table
    compatibile with posix systems, and nt
    '''
    searchstr = eth_addr.replace(
        ':', '.?') if eth_addr[2] == ':' else eth_addr.replace('-', '.?')
    try:
        output = Popen(['arp', '-a'], stdout=PIPE,
                       stderr=PIPE).communicate()[0].decode('utf-8')
        for line in output.strip().split('\n'):
            if re.search(searchstr, line):
                return line.split()[0]
    except FileNotFoundError:
        arp_cache: str = '/proc/net/arp'
        if path.exists(arp_cache):
            with open(arp_cache, 'r') as file:
                for line in file.readlines()[1:]:
                    line = line.strip()
                    if re.search(searchstr, line):
                        return line.split()[0]
        else:
            return None