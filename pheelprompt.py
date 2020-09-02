from playbooks.enumerate.basic_host_information import EnumerateBasicHostInformation

def prompt(pheelshell=None):
    prompt_str = '[(pheelpwn)]> '
    if pheelshell:
        basic_host_information = pheelshell.get_playbook(EnumerateBasicHostInformation)
        victim_user = basic_host_information.get_user()
        victim_hostname = basic_host_information.get_hostname()
        prompt_str = f'[{victim_user}@{victim_hostname} (pheelpwn)]> '

    while True:
        command = input(prompt_str).strip()
        if command == 'show enumerate EnumerateBasicHostInformation':
            if pheelshell:
                print(str(pheelshell.get_playbook(EnumerateBasicHostInformation)))
            else:
                print('Must be connected to a system in order to run this command!')
        elif command == 'quit' or command == 'exit':
            exit()
        else:
            print(f'Unrecognized command: "{command}"')

def main():
    prompt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b\r')
