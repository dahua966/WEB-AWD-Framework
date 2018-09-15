#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scapy.all import *
import sys

CUI = False
HOST = '172.10.10.11'

if CUI and len(sys.argv) < 2:
    print "python pcap_analysis.py <pcap name>"

filename = sys.argv[1]


def parse(pcap,menu):
    table = {}
    for i in range(len(pcap)):
        try:
            if pcap[i][Raw].load:
                payload = pcap[i][Raw].load
            else:
                payload = ""

            if pcap[i][IP].src == HOST:
                ip_addr = pcap[i][IP].dst
            elif pcap[i][IP].dst == HOST:
                ip_addr = pcap[i][IP].src
                
            table[ip_addr].append(payload)
        except IndexError:
            pass
        except KeyError:
            table[ip_addr] = []
            pass
    for key,value in table.items():
        fp = open("log/"+menu+'/'+key+".txt","w")
        for payload in value:
            fp.write("\r\n")
            fp.write(payload)
        fp.close()


if __name__ == '__main__':
    if CUI:
        filename = sys.argv[1]
    filename = '2018-09-05-1.pcap'
    pcap = rdpcap(filename)
    parse(pcap,filename[:filename.index('.')])