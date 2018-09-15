import re
import threading
import sys
import os


from time import sleep, time
from random import random

from auxiliary import *
#import psutil
#from psutil import process_iter

if sys.version_info.major == 2:
    from Queue import Queue
elif sys.version_info.major == 3:
    from queue import Queue
else:
    print('python2 or python3 required')
    exit()


ACTION_KILL = 0
ACTION_PASS = 1
ACTION_NEXT = 2
ACTION_INFO = 3
ACTION_ERRO = 4
ACTION_NONE = 5

class PsGuard(object):
    def __init__(self):
        self.interval = 0.1
        
        self.filters = [self.pass_pids_filter]
        self.counter = 0
        self.pass_pids = []
        self.pass_pids_refresh = 20
    
    def thread_loop(self):
        pass

    def run(self):
        while True:
            self.counter = (self.counter + 1) % self.pass_pids_refresh
            if self.counter == 0: self.pass_pids = []
            self.loop()
            interval = random()*self.interval*2
            sleep(interval)
            
    def speed_test(self, count):
        print(time())
        i = 0
        while True:
            i += 1
            self.counter = (self.counter + 1) % self.pass_pids_refresh
            if self.counter == 0: self.pass_pids = []
            self.loop()
            if i >= count:
                break
            
        print(time())
        exit()
            
    def loop(self):
        for process in process_iter():
            self.routine(process)
     
    def routine(self, process):
        action = self.process_handler(process)
        result = self.action_handler(process, action)
        self.log_handler(result)
            
    def process_handler(self, process):
        try:
            for func in self.filters:
                    action = func(process)
                    if action == ACTION_NEXT:
                        pass
                    else:
                        return action
            return ACTION_NONE
        except:
            return ACTION_ERRO
            
        
        
        
    def action_handler(self, process, action):
        if action == ACTION_PASS:
            self.pass_pids.append(process.pid)
        elif action == ACTION_KILL:
            process.kill()
            return 'kill {}:{}'.format(process.pid, process.name())
        elif action == ACTION_INFO:
            return 'info {}:{}'.format(process.pid, process.name())
        elif action == ACTION_ERRO:
            return 'erro {}:{}'.format(process.pid, 'no access or process exited')
        else:
            pass
    def log_handler(self, result):
        if result:
            print(result)
            
        
    def add_filter(self, func):
        self.filters.append(func)
        
    def pass_pids_filter(self, process):
        if process.pid in self.pass_pids:
            return ACTION_PASS
        else:
            return ACTION_NEXT
    
if __name__ == '__main__':
    def user_filter(process):
        ignore_lst = ['root','systemd-timesync','messagebus']
        if process.username() in ignore_lst:
            #print('ignore:',process.username())
            return ACTION_PASS
        else:
            return ACTION_NEXT
    
    def name_filter(process):
        ignore_lst = ['sh', 'bash']
        forbid_lst = ['torj','test_torj', 'exe', 'backdoor', ]
        name = process.name()
        if name in ignore_lst:
            return ACTION_PASS
        elif name in forbid_lst:
            return ACTION_KILL
        else:
            return ACTION_NEXT
        
    def python_restrict(process):
        allowed = ['server.py', 'psguard.py']
        name = process.name()
        if 'python' in name:
            cmdline = process.cmdline()
            if cmdline[0] != name:
                return ACTION_KILL
            elif len(cmdline) >= 2:
                if cmdline[1] in allowed:
                    return ACTION_PASS
                else:
                    return ACTION_KILL
            else:
                return ACTION_NEXT
        return ACTION_NEXT

    def www_data_kill(process):
        allowed = ['apache2','sh']  
        if process.username() == 'www-data' and process.name() not in allowed:
            return ACTION_KILL
        else:
            return ACTION_PASS
        
        
    pg = PsGuard()
    pg.interval = 0.1
    pg.add_filter(user_filter)
    # pg.add_filter(name_filter)
    # pg.add_filter(python_restrict)
    pg.add_filter(www_data_kill)
    pg.run()
    #pg.speed_test(1000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    