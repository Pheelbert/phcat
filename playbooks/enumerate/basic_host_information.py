from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateBasicHostInformation(Playbook):
    @staticmethod
    def description():
        return 'Executes commands to obtain user, hostname, and operating system.'

    def __init__(self):
        super().__init__()
        self.output_map = {}

    def __str__(self):
        output = '[host information]\n'
        for command, command_output in self.output_map.items():
            output += f' - {command}: {command_output}\n'

        return output

    def get_user(self):
        user_command = 'whoami'
        if user_command in self.output_map:
            return self.output_map[user_command]

        print('You need to run the playbook in order to access the victim user.')
        return None

    def get_hostname(self):
        hostname_command = 'hostname'
        if hostname_command in self.output_map:
            return self.output_map[hostname_command]

        print('You need to run the playbook in order to access the victim hostname.')
        return None

    def run(self, shell: Pheelshell):
        whoami_command = 'whoami'
        output = shell.execute_command(whoami_command, expect_single_line_output=True)
        if output == 'root':
            shell.add_hint('You\'re the root user! Congrats!')

        self.output_map[whoami_command] = output

        hostname_command = 'hostname'
        output = shell.execute_command(hostname_command, expect_single_line_output=True)
        self.output_map[hostname_command] = output

        os_command = 'uname -a'
        output = shell.execute_command(os_command, expect_single_line_output=True)
        self.output_map[os_command] = output

        self._has_run = True
