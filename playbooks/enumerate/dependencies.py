from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateDependencies(Playbook):
    @staticmethod
    def description():
        return 'Executes \'which\' on a list of useful binary names to determine if they are available.'

    def __init__(self):
        super().__init__()
        self.interesting_binaries = [
            'nc',
            'python3'
        ]
        self.available_binaries_map = {}

    def __str__(self):
        output = '[identified dependencies]\n'
        for binary, path in self.available_binaries_map.items():
            output += f' - {binary}: {path}\n'

        return output

    def is_binary_available(self, binary_name: str) -> str:
        if binary_name in self.available_binaries_map:
            return self.available_binaries_map[binary_name]

        return None

    def run(self, shell: Pheelshell):
        for binary in self.interesting_binaries:
            which_command = f'which {binary}'
            output = shell.execute_command(which_command, expect_single_line_output=True)
            if output:
                self.available_binaries_map[binary] = output

        self._has_run = True
