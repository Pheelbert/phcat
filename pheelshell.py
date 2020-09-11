import os.path
from typing import Type
from playbooks.playbook import Playbook
from pwnlib_socket_wrapper import PwnlibSocketWrapper

class Pheelshell():
    def __init__(self, socket: PwnlibSocketWrapper):
        self.socket = socket
        self.playbooks = {}
        self.hints = []

    def start_interactive(self):
        # TODO: Not working
        self.socket.client.interactive()

    def execute_command(self, command: str, expect_single_line_output=False) -> str:
        command_bytes = command.encode()
        output = self.socket.send_command_read_output(command_bytes, expect_single_line_output)
        return output

    def download(self, remote_path: str, local_path: str):
        if self.socket.remote_file_exists(remote_path):
            if self.socket.remote_file_readable(remote_path):
                remote_file_contents = self.socket.read_remote_file(remote_path)
            else:
                return f'\'{remote_path}\' not readable by current user!'
        else:
            return f'\'{remote_path}\' doesn\'t exist on the remote system!'

        try:
            with open(local_path, 'w') as local_file:
                local_file.write(remote_file_contents)

            return f'Downloaded remote file \'{remote_path}\' to \'{local_path}\' locally.'
        except IOError:
            return f'Could not open \'{local_path}\' due to IO error'
    
    def upload(self, local_path: str, remote_path: str):
        if not os.path.exists(local_path):
            return f'Local file \'{local_path}\' doesn\'t exist!'

        if self.socket.remote_file_exists(remote_path) and not self.socket.remote_file_writable(remote_path):
            return f'Remote file \'{remote_path}\' already exists and is not writable!'

        content = None
        with open(local_path, 'r') as local_file:
            content = local_file.read()

        self.socket.write_remote_file(remote_path, content)

        if self.socket.remote_file_exists(remote_path):
            return f'Uploaded local file \'{local_path}\' to remote \'{remote_path}\'!'

    def run_playbook(self, playbook: Type[Playbook]):
        playbook.run(self)
        playbook_class_name = playbook.__class__.__name__
        self.playbooks[playbook_class_name] = playbook

    def get_playbook(self, playbook_class: type) -> Playbook:
        playbook_class_name = playbook_class.__name__
        if playbook_class_name in self.playbooks:
            return self.playbooks[playbook_class_name]

        return None

    def get_hints(self):
        return self.hints

    def add_hint(self, hint: str):
        if hint not in self.hints:
            self.hints.append(hint)
