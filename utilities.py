import re
from typing import List
import netifaces

def fetch_ipv4_addresses() -> List[str]:
    ip_list = set()
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address = link['addr']
                if address != '127.0.0.1':
                    ip_list.add(address)

    return list(ip_list)

def escape_ansi(line: str) -> str:
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)
