from typing import Type
from playbooks.playbook import Playbook
from pwnlib_socket_wrapper import PwnlibSocketWrapper

class Pheelshell():
    def __init__(self, socket_wrapper: PwnlibSocketWrapper):
        self.socket_wrapper = socket_wrapper
        self.playbooks = {}

    def execute_command(self, command: str, single_line_output=False) -> str:
        if single_line_output:
            return self.socket_wrapper.send_command_read_output(command.encode(), single_line_output=True)
        else:
            return self.socket_wrapper.send_command_read_cached_temporary_file(command.encode())

    def run_playbook(self, playbook: Type[Playbook]):
        playbook.run(self)
        playbook_class_name = playbook.__class__.__name__
        self.playbooks[playbook_class_name] = playbook

    def get_playbook(self, playbook_class: type) -> Playbook:
        playbook_class_name = playbook_class.__name__
        if playbook_class_name in self.playbooks:
            return self.playbooks[playbook_class_name]

        return None
