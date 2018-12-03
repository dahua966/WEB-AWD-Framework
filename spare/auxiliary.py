import os
import re
import pwd
     
_uids_re = re.compile(br'Uid:\t(\d+)\t(\d+)\t(\d+)')
_name_re = re.compile(br'Name:\t(.*)\n')
_ppid_re = re.compile(br'PPid:\t(\d+)')


class Process(object):
    def __init__(self, pid):
        self.pid = pid
        self.proc_exe = ''
        self.proc_root = ''
        self.proc_cwd = ''
        self.proc_status = ''
        self.proc_cmdline = ''
        

            
    def path(self):
        if self.proc_exe == '':
            self.proc_exe = os.path.realpath('/proc/{}/exe'.format(self.pid))
        return self.proc_exe
    def exe(self):
        if self.proc_exe == '':
            self.proc_exe = os.path.realpath('/proc/{}/exe'.format(self.pid))
        return self.proc_exe
        
    def cwd(self):
        if self.proc_cwd == '':
            self.proc_cwd = os.path.realpath('/proc/{}/cwd'.format(self.pid))
        return self.proc_cwd
        
        
    def root(self):
        if self.proc_root == '':
            self.proc_root = os.path.realpath('/proc/{}/root'.format(self.pid))
        return self.proc_root
        
    def username(self):
        if self.proc_status == '':
            with open('/proc/{}/status'.format(self.pid)) as f:
                self.proc_status = f.read()
        real, effective, saved = _uids_re.findall(self.proc_status)[0]
        try:
            return pwd.getpwuid(int(real)).pw_name
        except KeyError:
            # the uid can't be resolved by the system
            return str(real)
        
    def cmdline(self):
        if self.proc_cmdline == '':
            with open('/proc/{}/cmdline'.format(self.pid)) as f:
                self.proc_cmdline = f.read().split('\x00')[:-1]
        return self.proc_cmdline
       
    def name(self):
        if self.proc_status == '':
            with open('/proc/{}/status'.format(self.pid)) as f:
                self.proc_status = f.read()
        return _name_re.findall(self.proc_status)[0]

    def ppid(self):
        if self.proc_status == '':
            with open('/proc/{}/status'.format(self.pid)) as f:
                self.proc_status = f.read()
        return _ppid_re.findall(self.proc_status)[0]

        
    
    def kill(self):
        os.kill(self.pid, 9)
    def __getattr__(self, attr):
        print('try to get:',attr)
        return None
        
def getpids():
    dirs = os.walk('/proc/').next()[1]
    pids = []
    for s in dirs:
        if s.isdigit():
            pids.append(int(s))
    return pids
            
def process_iter():
    pids = getpids()
    ret = []
    for pid in pids:
        try:
            p = Process(pid)
            ret.append(p)
        except Exception as e:
            #print(pid, e)
            pass
            
    return ret
    
if __name__ == '__main__':
    p = Process(28334)
    print(p.name())
    print(p.path())
    print(p.username())
    print(p.cmdline())
    print(p.ppid())