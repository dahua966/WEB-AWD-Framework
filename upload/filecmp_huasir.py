#!/usr/bin/python
# -*- coding: utf-8 -*-
__auth__ = 'HuaSir'
__url__ = 'huasir.me'

import filecmp
from os import *
from shutil import *
import difflib
import time

homedir = "/home/huasir"
bakfile = homedir+'/bak'
nowfile = '/var/www/html'
newfile = homedir+'/new'

strict = False

def getinput():
    if strict:
        j = 'y'
        print j
    j = raw_input('[?]recover or not(y/n)')
    while j != 'y' and j != 'n':
        j = raw_input('[?]recover or not(y/n)')
    return j

def filecompare(srcfile,basefile):
    src = file(srcfile).read().split(' ')
    base = file(basefile).read().split(' ')

    # ignore blank lines
    s = difflib.SequenceMatcher( lambda x: len(x.strip()) == 0,base, src) 
    
    lstres = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            lstres += "\n"
            pass
        elif  tag == 'delete' : 
            lstres.append('DELETE (line: %d)' % i1)
            lstres += base[i1:i2]
            lstres += "\n"
            lstres.append(' ')
        elif tag == 'insert' :    
            lstres.append('Insert (line: %d)' % j1)
            lstres += src[j1:j2]
            lstres += "\n"
            lstres.append(' ')
        elif tag == 'replace' :   
            lstres.append("Before: \n(line: %d) " % j1)
            lstres += src[j1:j2]
            lstres += "\n" 
            lstres.append("REPLACE:\n")
            lstres.append("After: \n(line: %d) " % i1)
            lstres += base[i1:i2]
            lstres += "\n"      
            lstres.append(' ')
        else:
            pass
    print (' '.join(lstres))

def detectnew(cmp,newfile):
    if cmp.right_only:
        for i in cmp.right_only:
            if path.isfile(path.join(cmp.right,i)):
                print ("[+]new file detect: %s" % path.join(cmp.right,i))   
                j = getinput()
                if (j == 'y'):
                    copy(path.join(cmp.right,i),newfile)
                    remove(path.join(cmp.right,i))
                    mkdir(path.join(cmp.right,i))
                    print ("[!]copy it to "+newfile+" and mkdir\n")
                elif (j == 'n'):
                    copy(path.join(cmp.right,i),cmp.left)
                    print ("[!]file uploaded successfully\n")
    for sub_cmp in cmp.subdirs.values():
            detectnew(sub_cmp,newfile)

def detectchange(cmp):
    for i in cmp.diff_files:
        print ("[*]file change detect: %s" % path.join(cmp.right,i))
        filecompare(path.join(cmp.left,i),path.join(cmp.right,i))
        j = getinput()
        if (j == 'y'):
            copy(path.join(cmp.left,i),cmp.right)
            print ("[!]file recovered successfully\n")
        elif (j == 'n'):
            copy(path.join(cmp.right,i),cmp.left)
            print ("[!]file uploaded successfully\n")

def detectdelete(cmp):
    if cmp.right_only:
        for i in cmp.left_only:
            print "file delete detect: %s" % path.join(cmp.left,i)
            copy(path.join(cmp.left,i),cmp.right)
            print "recovery file successfully"
    for sub_cmp in cmp.subdirs.values():
            detectdelete(sub_cmp)

def main():
    c = filecmp.dircmp(bakfile,nowfile)
    # detectchange(c)
    detectnew(c,newfile)

if __name__ == '__main__':
    print ("------------------File system watcher working------------------")
    print ("~~~~~~~~~~~~~~~~~~~~~~~Powered by HuaSir~~~~~~~~~~~~~~~~~~~~~~~")
    try:
    	if not path.isdir(newfile) or not path.isdir(bakfile):
    		raise Error
    except Exception as e:
    	print ("[!]Prepare work meet some problem")
    	print (e)
    print ("[+]Prepare work is ready")

    while True:
        try:
            main()
        except Exception as e:
            print (e.message)
        finally:
            time.sleep(5)