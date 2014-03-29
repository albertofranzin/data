#!/usr/bin/python -w

import subprocess
import sys
import re

def timestamp_to_secs(s):
    minsecs = s.rstrip("s").split('m')
    mins = int(minsecs[0])
    secmills = minsecs[1].split('.')
    return float(str(mins*60 + int(secmills[0])) + "." + secmills[1])

file_mine = sys.argv[1]
#file_gobn = sys.argv[2]

with open(file_mine, "r") as myfile:
    lines = myfile.readlines()
    for line in lines:
        if line[0] == '*':
            row = line.rstrip('\n').replace('+','').replace('%','').split(' ')
            row = filter(None, row)
            try:
                row.remove('*')
                row.remove("integral")
                row.remove('0')
            except:
                pass
            #print row
            #print row[0],',', row[2],',', row[3],',', row[5],',' #'\\\\'
            print row[3]#, row[2], row[3], row[5]
