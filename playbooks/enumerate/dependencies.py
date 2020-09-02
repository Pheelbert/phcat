class EnumerateDependencies:
    def __init__(self):
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

    def is_binary_available(self, binary_name):
        if binary_name in self.available_binaries_map:
            return self.available_binaries_map[binary_name]

        return None

    def run(self, shell):
        for binary in self.interesting_binaries:
            which_command = f'which {binary}'
            output = shell.send_command_read_output(which_command.encode(), single_line_output=True)
            if output:
                self.available_binaries_map[binary] = output
