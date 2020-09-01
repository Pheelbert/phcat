class EnumerateSudoList:
    def __init__(self):
        self.interesting_lines = []

    def __str__(self):
        output = 'Sudo rights for current user:\n'
        for line in self.interesting_lines:
            output += f' - {line}\n'

        return output

    def run(self, pheelshell):
        sudo_list_command = 'sudo -l'
        output = pheelshell.send_command_read_cached_temporary_file(sudo_list_command.encode())
        self._parse(output)

    def _parse(self, output):
        interesting_flag = False
        for line in output.split('\n'):
            if 'may run the following commands' in line:
                interesting_flag = True
                continue

            if not line:
                interesting_flag = False

            if interesting_flag:
                self.interesting_lines.append(line.strip())
