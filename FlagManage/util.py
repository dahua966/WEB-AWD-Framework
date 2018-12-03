#-*-coding:utf-8 -*-
import re
import requests
import time
from pyquery import PyQuery as PQ
from dbinit import Flag,db,Success
import traceback  
from log import Log

DEBUG = False
CHECK = False
#huasir
PATTERN = '[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}'
FLAGURL = "https://172.16.4.1/Common/awd_sub_answer"
# FLAGURL = "http://127.0.0.1/"
TOKEN = '29f227503044c6e8adefa89ceebfc434'

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def postflag(flag):
    try:  
        flag = flag.strip()
        Log.info("Submitting flag: "+flag)
        if Success.ifexist(flag) > 0:
            Log.error("This flag has been submited successfully!")
            return "[!]This flag has been submited successfully!\r\n"
        if CHECK and not checkflag(flag):
            Log.error('Wrong flag format')
            return "[!]Wrong flag format\r\n"
        retry = 0
        for i in range(3):
            #,verify=False
            res = requests.post(url=FLAGURL,data={"answer":flag,"token":TOKEN},timeout=3).content
            # print res
            #判断条件
            if '"status":1' in res:
                db.add(Success(flag=flag,stime=int(time.time())))
                db.commit()
                Log.success('Submit Success')
                return "[+]Submit Success\r\n"
            else:
                Log.warning('Submit Fail, try again for the %d times' % (i+1))
        Log.error('Submit failed for 3 times, flag will be log into database')
        raise RuntimeError('FlagError')
    except:
        if DEBUG:
            print traceback.print_exc()
        try:
            if Flag.ifexist(flag) == 0:
                db.add(Flag(flag=flag,stime=int(time.time())))
                db.commit()
            else:
                Log.wait("This flag has been insert into db, you should resubmit")
                return "[!]This flag has been insert into db, you should resubmit\r\n"
        except:
            # print traceback.print_exc()
            Log.error("Submit flag failed and insert into db error")
            return "[!]Submit flag failed and insert into db error\r\n"
        Log.wait("Submit flag failed and insert into db")
        return "[!]Submit flag failed and insert into db\r\n"

def checkflag(flag):
    res = re.findall(PATTERN,flag)
    if len(res)>0:
        return True
    else:
        return False

def resubmitflag():
    res = []
    Flag.clear()
    reflags = Flag.getflag()
    if not reflags:
        Log.warning('No flag need to be resubmited')
    for rf in reflags:
        Log.wait('Resubmiting flag: %s' % rf)
        postflag(rf)

def gettoken(html):
    token_name = "token"
    dom = PQ(html)
    form = dom("form")
    token = str(PQ(form)("input[name=\"%s\"]" % token_name).attr("value")).strip()
    return token

def cmd_server():
    while True:
        cmd = raw_input('# ')
        if cmd.startswith('submit '):
            flag_str = cmd[7:].strip()
            postflag(flag_str)
        elif cmd.startswith('resubmit'):
            try:
                resubmitflag()
            except:
                Log.warning("resubmit flag failed")
        elif cmd.startswith('clear'):
            try:
                Success.clear()
            except:
                Log.warning("clear success table failed")
        elif cmd.startswith('exit'):
            break
        elif cmd == 'help' or cmd == '?':
            print '''
            submit [flag]   submit a flag specially
            resubmit        resubmit all flag in db
            clear           clear success table
            exit            exit
            '''
        else:
            print "help(?)"

def main():
    flag = []
    for f in flag:
        postflag(f)

if __name__ == '__main__':
    main()