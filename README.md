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
usage: remly.py [-h] -m ETHERNET_ADDRESS [-p PORT] [-b BROADCAST]

Turn on your computer remotely

optional arguments:
  -h, --help           show this help message and exit
  -m ETHERNET_ADDRESS  device ethernet address
  -p PORT              port for WoL protocol (default: 9)
  -b BROADCAST         broadcast address (default: 192.168.0.255)
```

#### library
```python
from remly import wake_up

wake_up(eth_addr="AA:AA:AA:AA:AA:AA", port=555, broadcast=['192.168.16.255'])

```
```python
from remly import wake_up

known_computers = {
    "dev1": "2b:56:ff:d3:3f:31",
    "dev2": "60:f4:4c:53:9a:7f"
}

for computer in known_computers:
    wake_up(eth_addr=computer, bcasts=['192.168.16.255'], port=9)

```

## Release History

* 1.0.51
    * code documentation.
    * upgrade mac verification function to support more physical addresses formats.
    * added future allows getting ip addres from mac (__get_ip_from_eth).
* 1.0.5
    * fixed a startup bug.
    * improve code.
    * removing unnecessary class.
* 1.0.0
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
