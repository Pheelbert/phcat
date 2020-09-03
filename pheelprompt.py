import re
from pheelshell import Pheelshell
from playbooks.enumerate.basic_host_information import EnumerateBasicHostInformation
from playbooks.enumerate.dependencies import EnumerateDependencies
from playbooks.enumerate.sudo_list import EnumerateSudoList

module_type_playbook_classes_map = {
    'enumerate': [
        EnumerateBasicHostInformation,
        EnumerateDependencies,
        EnumerateSudoList
    ]
}

def prompt(pheelshell: Pheelshell=None):
    prompt_str = '[Offline (pheelpwn)]> '
    if pheelshell:
        basic_host_information = pheelshell.get_playbook(EnumerateBasicHostInformation)
        victim_user = basic_host_information.get_user()
        victim_hostname = basic_host_information.get_hostname()
        prompt_str = f'[{victim_user}@{victim_hostname} (pheelpwn)]> '

    while True:
        command = input(prompt_str).strip()
        if command == 'quit' or command == 'exit':
            exit()
        elif command == 'show hints':
            if not pheelshell:
                print('Must be connected to a victim in order to show hints.')
                continue

            hints = pheelshell.get_hints()
            for index, hint in enumerate(hints):
                print(f'[hint #{index + 1}]')
                print(hint)

            continue

        matches = re.search(r'(?P<action>.*) (?P<type>.*) (?P<index>[0-9]+)', command)
        if not matches:
            matches = re.search(r'(?P<action>.*) (?P<type>.*)', command)

        if not matches:
            print(f'Unrecognized command: "{command}"')
            continue

        action = matches.group('action')
        if action != 'show':
            print(f'Unrecognized action in command: "{command}"')
            continue

        module_type = matches.group('type')
        if module_type not in module_type_playbook_classes_map:
            print(f'Unrecognized module type in command: "{command}"')
            continue

        module_index = int(matches.group('index')) - 1 if len(matches.groups()) == 3 else None
        if module_index and (module_index < 0 or module_index >= len(module_type_playbook_classes_map[module_type])):
            print(f'Module index for {module_type} is out of range: {module_index + 1}')
            continue

        if action and module_type:
            if module_index is not None:
                if not pheelshell:
                    print('Must be connected to a victim in order to show playbook results.')
                    continue
                else:
                    playbook_class = module_type_playbook_classes_map[module_type][module_index]
                    playbook = pheelshell.get_playbook(playbook_class)
                    module_output = str(playbook)
                    print(module_output)
            else:
                for index, playbook_class in enumerate(module_type_playbook_classes_map[module_type]):
                    playbook = pheelshell.get_playbook(playbook_class) if pheelshell else None
                    status = 'X' if playbook and playbook.has_run() else ' '
                    description = playbook_class.description()
                    print(f'{index + 1}. [{status}] {playbook_class.__name__}: {description}')

def main():
    prompt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b\r')
