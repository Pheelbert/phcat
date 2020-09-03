from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateSudoList(Playbook):
    def __init__(self):
        self.interesting_lines = []

    def __str__(self):
        output = '[sudo list]\n'
        for line in self.interesting_lines:
            output += f' - {line}\n'

        return output

    def run(self, shell: Pheelshell):
        sudo_list_command = 'sudo -l'
        output = shell.execute_command(sudo_list_command)
        self._parse(output)

    def _parse(self, output: str) -> str:
        interesting_flag = False
        for line in output.split('\n'):
            if 'may run the following commands' in line:
                interesting_flag = True
                continue

            if not line:
                interesting_flag = False

            if interesting_flag:
                self.interesting_lines.append(line.strip())
