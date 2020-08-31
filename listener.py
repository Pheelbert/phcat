import pwn

EXPECTED_PROMPT = b'$ '
LISTENING_PORT = 9001
COMMAND_TIMEOUT = 1 # Waits at least 1 second when 'until' string doesn't match

def main():
    commands = [
        'whoami',
        'hostname',
        'uname -a',
        'sudo -l'
    ]

    commands_output = {}
    with pwn.listen(LISTENING_PORT).wait_for_connection() as client:
        for command in commands:
            output = send_command_read_output(client, command.encode())
            commands_output[command] = output

        #client.interactive()
    
    for command, output in commands_output.items():
        print(f'{command}\n--------\n{output}\n--------\n')

def ignore_until_prompt(client, prompt=EXPECTED_PROMPT):
    if not isinstance(prompt, bytes):
        print('Prompt must be bytes')
        exit()

    client.recvuntil(prompt)

def send_command(client, command):
    if not isinstance(command, bytes):
        print('Command must be bytes')
        exit()

    client.sendline(command)

def send_command_read_output(client, command, prompt=EXPECTED_PROMPT, timeout=COMMAND_TIMEOUT):
    if not isinstance(command, bytes):
        print('Command must be bytes')
        exit()

    if not isinstance(prompt, bytes):
        print('Prompt must be bytes')
        exit()

    ignore_until_prompt(client, prompt)
    client.sendline(command)
    client.recvuntil(b'\n')

    output = ''
    while True:
        output_line = client.recvuntil(b'\n', timeout=timeout).decode('utf-8')
        if not output_line:
            break

        output += output_line

    return output.strip()

if __name__ == '__main__':
    main()

