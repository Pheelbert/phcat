import re
from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateSudoList(Playbook):
    @staticmethod
    def description():
        return 'Executes \'sudo -l\' to determine if there is an easy privilege escalation.'

    def __init__(self):
        super().__init__()
        self.output = None

    def __str__(self):
        return '[sudo -l]\n' + self.output

    def _parse(self, output: str) -> str:
        for line in output.split('\n'):
            matches = re.findall(r'\((.*) : (.*)\) (.*): (.*)', line)
            if matches:
                user = matches[0][0]
                group = matches[0][1]
                nopasswd = matches[0][2]
                binary = matches[0][3]
                if nopasswd == 'NOPASSWD' and binary == 'ALL':
                    return f'You can run all commands as user {user} and group {group} by running \'sudo -u {user} /bin/bash\'.'

        return None

    def run(self, shell: Pheelshell):
        sudo_list_command = 'sudo -l'
        output = shell.execute_command(sudo_list_command)
        self.output = output
        hint = self._parse(output)
        if hint:
            shell.add_hint(hint)

        self._has_run = True
