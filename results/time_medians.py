#!/usr/bin/python -w

def median(l):
    s = sorted(l)
    length = len(s)
    if length % 2 == 1:
        return (s[length / 2] + s[length / 2 - 1]) / 2.0
    else:
        return s[length / 2]

preprocessing = {}
execution = {}
total = {}
with open("time/time_eocp.txt", "r") as of:
    lines = of.readlines()
    for line in lines:
        times = line.rstrip('\n').split(' | ')
        tto = times[0].split('_')
        times[0] = tto[0]+'_'+tto[1]
        if not times[1] in ["", " "] and \
           not times[2] in ["", " "] and \
           not times[3] in ["", " "] and \
           not times[4] in ["", " "]:
            if times[0] in preprocessing:
                preprocessing[times[0]].extend([float(times[1])-float(times[4])])
            else:
                preprocessing[times[0]] = list()
                preprocessing[times[0]].extend([float(times[1])-float(times[4])])
            if times[0] in execution:
                execution[times[0]].extend([float(times[4])])
            else:
                execution[times[0]] = list()
                execution[times[0]].extend([float(times[4])])
            if times[0] in total:
                total[times[0]].extend([float(times[1])])
            else:
                total[times[0]] = list()
                total[times[0]].extend([float(times[1])])
    #print preprocessing

for key in preprocessing:
    filter(None, preprocessing[key])
    filter(None, execution[key])
    filter(None, total[key])
    if len(preprocessing[key]) > 0:
        preprocessing[key] = median(preprocessing[key])
    else:
        preprocessing[key] = '-'
    if len(execution[key]) > 0:
        execution[key] = median(execution[key])
    else:
        execution[key] = '-'
    if len(total[key]) > 0:
        total[key] = median(total[key])
    else:
        total[key] = '-'

for key in preprocessing:
    print key, " & ", preprocessing[key], " & ", execution[key], " & ", total[key], "\\\\"

