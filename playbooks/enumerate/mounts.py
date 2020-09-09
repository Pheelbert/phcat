import re
from typing import List, Tuple
from pheelshell import Pheelshell
from playbooks.playbook import Playbook

class EnumerateMounts(Playbook):
    @staticmethod
    def description():
        return 'Checks \'mount\' output for any interesting mount points on the system.'

    def __init__(self):
        super().__init__()
        self.interesting_mount_tuples = []
        self.not_interesting_strings = [
            '/lib/live/mount/persistence',
            '/lib/live/mount/rootfs'
        ]

    def __str__(self):
        output = 'No interesting mount points.'
        if self.interesting_mount_tuples:
            output = '[interesting mounts]\n'
            for mount_device, mount_point in self.interesting_mount_tuples:
                output += f'{mount_device} on {mount_point}\n'

            output = output[:-1]

        return output
    
    def _not_interesting_mount_point(self, mount_point):
        for string in self.not_interesting_strings:
            if string in mount_point:
                return True

        return False

    def _parse(self, output) -> List[Tuple[str, str]]:
        interesting_mount_tuples = []
        for line in output.split('\n'):
            matches = re.search(r'(?P<mounted>.*) on (?P<mount_point>.*) type', line)
            if matches:
                mounted_device = matches.group('mounted')
                mount_point = matches.group('mount_point')

                # Ignore whatever doesn't have a path, not sure what those are *noob_face*
                if '/' in mounted_device and '/' in mount_point and not self._not_interesting_mount_point(mount_point):
                    interesting_mount_tuples.append((mounted_device, mount_point))

        return interesting_mount_tuples

    def run(self, shell: Pheelshell):
        output = shell.execute_command('mount')
        self.interesting_mount_tuples = self._parse(output)
        interesting_mounts_count = len(self.interesting_mount_tuples)
        if interesting_mounts_count:
            hint = f'Found {interesting_mounts_count} interesting mount points. Try looking in them or running \'strings <mounted_device>\'.'
            shell.add_hint(hint)

        self._has_run = True
