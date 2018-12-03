import hashlib
import sys

passwd = open('password.txt','rb').readlines()

if len(sys.argv)<2:
	print "Usage:"
	print "python cmd5.py hash_value"
	break
else:
	md5 = sys.argv[1]
for p in passwd:
	if hashlib.md5(p.strip()).hexdigest() == md5:
		print "key found: " + p
		exit
		
		