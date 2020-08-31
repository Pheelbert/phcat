import pwn

EXPECTED_PROMPT = b'$ '
LISTENING_PORT = 9001

def main():
    with pwn.listen(LISTENING_PORT).wait_for_connection() as client:
        whoami = send_command_read_output(client, b'whoami')
        hostname = send_command_read_output(client, b'hostname')
        uname = send_command_read_output(client, b'uname -a')
        print(f'whoami -> {whoami}')
        print(f'hostname -> {hostname}')
        print(f'uname -> {uname}')
        #client.interactive()

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

def send_command_read_output(client, command, prompt=EXPECTED_PROMPT):
    if not isinstance(command, bytes):
        print('Command must be bytes')
        exit()

    if not isinstance(prompt, bytes):
        print('Prompt must be bytes')
        exit()

    ignore_until_prompt(client, prompt)
    client.sendline(command)
    client.recvuntil(b'\n')
    output_bytes = client.recvuntil(b'\n')
    output_decoded = output_bytes.decode("utf-8")
    return output_decoded.strip()

if __name__ == '__main__':
    main()

