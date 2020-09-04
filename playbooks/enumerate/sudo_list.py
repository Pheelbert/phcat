import re
from re import findall
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

    def _parse(self, output: str, shell: Pheelshell) -> str:
        for line in output.split('\n'):
            if line.strip() in ['(ALL : ALL) ALL', '(ALL : ALL) NOPASSWD: ALL', '(ALL) NOPASSWD: ALL']:
                shell.add_hint('You can run all commands as root by running \'sudo su\' or \'sudo -i\'')
                continue

            matches = re.findall(r'\((.*)\) (.*): (.*)', line)
            if matches:
                user = matches[0][0]
                group = None
                if ' : ' in user:
                    user, group = user.split(' : ')

                user_group_str = f'{user}'
                if group:
                    user_group_str = f'{user}:{group}'

                nopasswd = matches[0][1]
                binary = matches[0][2]

                if nopasswd == 'NOPASSWD':
                    which_command = f'which {binary}'
                    which_output = shell.execute_command(which_command)
                    if which_output:
                        shell.add_hint(f'Check GTFOBins for \'{binary}\'. Running this binary can provide \'{user_group_str}\' access when run \'sudo -u {user} {binary}\'.')
                    else:
                        if binary == 'ALL':
                            shell.add_hint(f'You can run all commands as user \'{user_group_str}\' by running \'sudo -u {user} /bin/bash\'.')
                        else:
                            shell.add_hint(f'Try to find a flaw in \'{binary}\' to gain \'{user}\' shell by running \'sudo -u {user} {binary}\'.')
                else:
                    print(f'DEBUG: Unexpected value for {nopasswd}. Please implement handling.')
                    exit()

    def run(self, shell: Pheelshell):
        sudo_list_command = 'sudo -l'
        output = shell.execute_command(sudo_list_command)
        self.output = output
        self._parse(output, shell)

        self._has_run = True
