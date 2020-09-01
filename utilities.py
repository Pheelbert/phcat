import netifaces

def fetch_ipv4_addresses():
    ip_list = set()
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address = link['addr']
                if address != '127.0.0.1':
                    ip_list.add(address)

    return list(ip_list)
