from typing import List, Tuple
from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateInterestingFiles(Playbook):
    @staticmethod
    def description():
        return 'Finds interesting files that your user has some access to.'

    def __init__(self):
        super().__init__()
        self.readable_files: List[str] = []
        self.writable_files: List[str] = []
        self.executable_files: List[str] = []
        self.interesting_directories = [
            '/home/'
        ]

    def __str__(self):
        output = '[interesting files]\n'
        if self.readable_files:
            output += '[readable]\n'
            output += '\n'.join(self.readable_files)
            output += '\n'

        if self.writable_files:
            output += '[writable]\n'
            output += '\n'.join(self.writable_files)
            output += '\n'

        if self.executable_files:
            output += '[executable]\n'
            output += '\n'.join(self.executable_files)

        return output
    
    def _parse_paths(self, output):
        lines = []
        for line in output.split('\n'):
            if ': Permission denied' not in line:
                lines.append(line)

        return lines

    def run(self, shell: Pheelshell):
        for interesting_directory in self.interesting_directories:
            readable_command = f'find {interesting_directory} -readable -type f'
            print(f'Finding readable files in \'{interesting_directory}\' by running \'{readable_command}\'')
            output = shell.execute_command(readable_command)
            parsed_output = self._parse_paths(output)
            if parsed_output:
                self.readable_files.extend(parsed_output)

            for filepath in parsed_output:
                if filepath.endswith('user.txt') or filepath.endswith('root.txt'):
                    shell.add_hint(f'Found readable HTB flag file: \'{filepath}\'')

            writable_command = f'find {interesting_directory} -writable -type f'
            print(f'Finding writable files in \'{interesting_directory}\' by running \'{writable_command}\'')
            output = shell.execute_command(writable_command)
            parsed_output = self._parse_paths(output)
            if parsed_output:
                self.writable_files.extend(parsed_output)

            executable_command = f'find {interesting_directory} -executable -type f'
            print(f'Finding executable files in \'{interesting_directory}\' by running \'{executable_command}\'')
            output = shell.execute_command(executable_command)
            parsed_output = self._parse_paths(output)
            if parsed_output:
                self.executable_files.extend(parsed_output)

            unreadable_executable_directory_command = f'find {interesting_directory} -executable -type d ! -readable'
            print(f'Finding executable directories that aren\'t readable in \'{interesting_directory}\' by running \'{unreadable_executable_directory_command}\'')
            output = shell.execute_command(unreadable_executable_directory_command)
            parsed_output = self._parse_paths(output)
            if parsed_output:
                self.executable_files.extend(parsed_output)
                for directory in parsed_output:
                    hint = (f'Current user has execute rights on directory \'{directory}\'\n'
                            f'This means you can guess filenames in the directory and run (for example) \'cat {directory}secret.txt\'.')
                    shell.add_hint(hint)

        self._has_run = True
