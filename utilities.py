import re
import subprocess
import sys
from threading import Thread
from typing import List
import netifaces

def fetch_ipv4_addresses() -> List[str]:
    ip_list = set()
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                address = link['addr']
                if address != '127.0.0.1':
                    ip_list.add(address)

    return list(ip_list)

def escape_ansi(line: str) -> str:
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def run_command_locally(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    retval = process.poll()

    while retval is None:
        for line in iter(process.stdout.readline, ''):
            sys.stdout.flush()

        retval = process.poll()

    retval = process.wait()
    if retval != 0:
        raise RuntimeError(f'\"{command}\" terminated with a non-zero exit code {retval}')
