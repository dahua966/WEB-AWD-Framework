import hackhttp
import re
from setting import PATTERN

hh = hackhttp.hackhttp(hackhttp.httpconpool(500))

file = open('log/127.0.0.1.txt').read()
logs = file.split('------------------------------------------------------------------------------')

for log in logs:
    try:
        (time,raws) = log.split('***********')
        raws = raws.strip()
        time = time.strip().split()[1].strip()
        # print time
        if time > '14:54:00' and time < '14:55:00':

            uri = re.findall('[POST|GET]\s(\S*)\sHTTP',raws)[0]
            
            _, _, html, _, log = hh.http('http://127.0.0.1'+uri, raw = raws, headers={"Local": "1"})
            #true paylaod or not
            # if 'flag' in html:
            print log['request']
            print '-'*100
    except Exception:
        print log
        pass


