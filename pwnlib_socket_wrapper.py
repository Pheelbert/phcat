import hashlib
import uuid
from numpy.ma.core import append
import pwn
from pwnlib.tubes.sock import sock
import utilities

class PwnlibSocketWrapper:
    def __init__(self, client: sock, attacker_ip: str):
        self.client = client
        self.attacker_ip = attacker_ip
        self.timeout = 1
        self.encoding = 'utf-8'
        self.netcat_file_transfer_port = 9002
        self.newline_bytes = b'\n'

    def synchronize_output(self):
        random = str(uuid.uuid1())
        random_echo_command_bytes = f'echo {random}'.encode()
        self.client.sendline(random_echo_command_bytes)
        self.client.recvuntil(random_echo_command_bytes + self.newline_bytes).decode(self.encoding)
        self.client.recvuntil(random.encode() + self.newline_bytes)
        self.client.clean()

    def send_command_read_output(self, command_bytes: bytes, expect_single_line_output=False) -> str:
        self.synchronize_output()
        self.client.sendline(command_bytes)
        self.client.recvuntil(command_bytes + self.newline_bytes)

        output = ''
        while True:
            output_line = self.client.recvuntil(self.newline_bytes, timeout=self.timeout).decode(self.encoding)
            output += output_line

            if not output_line or expect_single_line_output:
                break

        ansi_escaped_output = utilities.escape_ansi(output)
        return ansi_escaped_output.strip()

    def read_remote_file(self, remote_path: str) -> str:
        cat_command = f'cat {remote_path}'.encode()
        file_contents = self.send_command_read_output(cat_command)
        return file_contents
    
    def write_remote_file(self, remote_path: str, content: str):
        if self.remote_file_exists(remote_path):
            print('File already exists, will overwrite...')
            self.delete_remote_file(remote_path)

        for line in content.split('\n'):
            append_line_command = f'echo \'{line}\' >> {remote_path}'.encode()
            self.client.sendline(append_line_command)

    def delete_remote_file(self, remote_path: str):
        remove_command = f'rm -rf {remote_path}'.encode()
        self.client.sendline(remove_command)

    def remote_file_exists(self, remote_path: str) -> bool:
        file_exists_command = f'file {remote_path}'.encode()
        output = self.send_command_read_output(file_exists_command, expect_single_line_output=True)
        return 'No such file or directory' not in output and ': empty' not in output

    def remote_file_readable(self, remote_path: str) -> bool:
        file_readable_command = f'find {remote_path} -readable'.encode()
        output = self.send_command_read_output(file_readable_command, expect_single_line_output=True)
        return not not output

    def remote_file_writable(self, remote_path: str) -> bool:
        file_writeable_command = f'find {remote_path} -writable'.encode()
        output = self.send_command_read_output(file_writeable_command, expect_single_line_output=True)
        return not not output
