class EnumerateBasicHostInformation:
    def __init__(self):
        self.commands = [
            'whoami',
            'hostname',
            'uname -a'
        ]
        self.output_map = {}

    def __str__(self):
        output = 'Host information:\n'
        for command, command_output in self.output_map.items():
            output += f' - {command}: {command_output}\n'

        return output

    def run(self, pheelshell):
        for command in self.commands:
            output = pheelshell.send_command_read_output(command.encode(), single_line_output=True)
            self.output_map[command] = output
