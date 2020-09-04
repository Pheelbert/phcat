from typing import Type
from playbooks.playbook import Playbook
from pwnlib_socket_wrapper import PwnlibSocketWrapper

class Pheelshell():
    def __init__(self, socket: PwnlibSocketWrapper):
        self.socket = socket
        self.playbooks = {}
        self.hints = []

    def execute_command(self, command: str, expect_single_line_output=False) -> str:
        command_bytes = command.encode()
        if expect_single_line_output:
            return self.socket.send_command_read_output(command_bytes, expect_single_line_output=True)
        else:
            return self.socket.send_command_read_output_through_temporary_file(command_bytes)

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
