from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateBasicHostInformation(Playbook):
    @staticmethod
    def description():
        return 'Executes commands to obtain user, hostname, and operating system.'

    def __init__(self):
        super().__init__()
        self.commands = [
            'whoami',
            'hostname',
            'uname -a'
        ]
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
        for command in self.commands:
            output = shell.execute_command(command, expect_single_line_output=True)
            self.output_map[command] = output
        
        self._has_run = True
