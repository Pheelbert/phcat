from typing import List, Dict
from pheelshell import Pheelshell
from playbooks.playbook import Playbook
from playbooks.file_permissions import FilePermissions

class EnumerateSUIDFiles(Playbook):
    @staticmethod
    def description():
        return 'Finds SUID files.'

    def __init__(self):
        super().__init__()
        self.suid_files = []
        self.file_permissions_dict: Dict[str, FilePermissions] = {}

    def __str__(self):
        output = 'No SUID files found.'
        if self.suid_files:
            output = '[SUID files]\n'
            for suid_file, file_permissions in self.file_permissions_dict.items():
                output += f'{suid_file}: {str(file_permissions)}\n'

        return output
    
    def _parse_paths(self, output) -> List[str]:
        lines = []
        for line in output.split('\n'):
            if line:
                lines.append(line)

        return lines

    def run(self, shell: Pheelshell):
        find_suid_command = f'find / -perm -u=s -type f 2>/dev/null'
        print(f'Finding SUID files...')
        output = shell.execute_command(find_suid_command)
        parsed_output = self._parse_paths(output)
        if parsed_output:
            self.suid_files = parsed_output
            suid_file_count = len(self.suid_files)
            print(f'Checking {suid_file_count} SUID files permissions...')
            for index, suid_file in enumerate(self.suid_files):
                print(f'Checking \'{suid_file}\'... ({index + 1}/{suid_file_count})')
                permissions_command = f'ls -l {suid_file}'
                output = shell.execute_command(permissions_command)
                file_permissions = FilePermissions(output)
                self.file_permissions_dict[suid_file] = file_permissions

                if file_permissions.can_others_execute():
                    if file_permissions.can_others_read():
                        shell.add_hint(f'SUID file \'{suid_file}\' is world readable!')
                    if file_permissions.can_others_write():
                        shell.add_hint(f'SUID file \'{suid_file}\' is world writable!')

        self._has_run = True
