from os import *
import re

PATTERN = 'flag\{.*\}'
def traversal(path='/tmp/log'):
    for dir,folder,files in walk(path):
        for f in files:
            t = "%s/%s"%(dir,f)
            yield t

def check(logs):
    for l in logs:
        with open(l) as log:
            line = 0
            for ll in log.readlines():
                line += 1
                if re.findall(ll,PATTERN):
                    print 'file: '+l
                    print "line: "+str(line)

if __name__ == '__main__':
    logs = traversal('..')
    for i in logs:
        print i
    # check(logs)