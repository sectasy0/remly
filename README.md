# Remly
> Small python library and CLI script which allows running computers remotely on LAN.

![Python version][python-image]

## Installation

```sh
pip install remly
```

## Usage example

A few motivating and useful examples of how remly can be used.

#### CLI program

```sh
usage: remly [-h] {s,w} ...

Cli script allow turn on your computer remotely and check status

positional arguments:
  {s,w}       commands
    s         check device status (accept ipv4 and mac)
    w         wake up computer

optional arguments:
  -h, --help  show this help message and exit
```

Wake up device
```sh
remly w -m AA:AA:AA:AA:AA:AA
```

```sh
usage: remly w [-h] [--mac ETH_ADDR] [--port PORT] [--bcasts BCASTS [BCASTS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --mac ETH_ADDR, -m ETH_ADDR
                        device physical address
  --port PORT, -p PORT  port for WoL protocol (default: 9)
  --bcasts BCASTS [BCASTS ...], -b BCASTS [BCASTS ...]
                        broadcast address (default: 192.168.0.255)
```

Check device status
```
remly s -m AA:AA:AA:AA:AA:AA
```

```sh
usage: remly s [-h] [--mac ETH_ADDR] [--ipv4 IP_ADDRESS] [--port PORT] [--timeout TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --mac ETH_ADDR, -m ETH_ADDR
                        device physical address
  --ipv4 IP_ADDRESS, -v4 IP_ADDRESS
                        device ipv4 address
  --port PORT, -p PORT  port for ICMP protocol (default: 7)
  --timeout TIMEOUT, -t TIMEOUT
```

#### library
```python
from remly import wake_up, status

# wake up device
wake_up(eth_addr='AA:AA:AA:AA:AA:AA', port=555, broadcast=['192.168.16.255'])

# check device status
# takes either an ip or a mac address
status(ip_address='192.168.16.5')

# based on physical address
status(eth_addr='2b:56:ff:d3:3f:31', timeout=5, port=1)

```
```python
from remly import wake_up

known_computers = {
    'dev1': '2b:56:ff:d3:3f:31',
    'dev2': '60:f4:4c:53:9a:7f'
}

for __, dev in known_computers.items():
    wake_up(eth_addr=dev, bcasts=['192.168.16.255'], port=9)

```

## Release History

* 2.0
    * code documentation.
    * upgrade mac verification function to support more physical addresses formats.
    * added future allows getting ip addres from mac (read_arptable).
    * added checking device status function.
* 1.0
    * release working program.

## Meta

Piotr Markiewicz – [@LinkedIn](https://www.linkedin.com/in/piotr-markiewicz-a44b491b1/) – sectasy0@gmail.coom

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/sectasy0](https://github.com/sectasy0)

## Contributing

1. Fork it (<https://github.com/sectasy0/remly>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/python-3.8-blue
[pypi-image]: https://img.shields.io/badge/pypi-remly-blue
[pypi-url]:  pypi.org/project/remly/
