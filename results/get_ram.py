#!/usr/bin/python -w

import subprocess
import sys
import re

def to_mega(m):
    #print "##", m
    if re.match("NA", m):
        #print "HALO"
        return m
    if m.count('M') == 1:
        return float(m.replace('M',''))
    if m.count('G') == 1:
        m = float(m.replace('G','')) * 1024
        return m

# get output files
ls_command    = "ls ../../mail_dei/cur/"
list_of_files = subprocess.Popen(ls_command, stdout=subprocess.PIPE, shell=True)
(output, err) = list_of_files.communicate()
output        = output.rstrip().split('\n')

outfile = open("memory/memres.txt", "w")

for f in output:
    with open("../../mail_dei/cur/"+f, "r") as resfile:
        textfile = resfile.read().replace('\n','')
        if textfile.count("From: root@dei.unipd.it (root)") > 0 and textfile.count("Max vmem") > 0 and textfile.count("STDIN") == 0:
            instance_num = textfile.split("(test.job)")[0].split("Job")[-1].strip('\n').strip('\t').strip(' ')
            if textfile.count("Aborted") > 0:
                instance_mem = textfile.split("failed assumedly after job because")[0].split("Max vmem")[1].split("=")[1]
            else:
                instance_mem = textfile.split("Exit Status")[0].split("Max vmem")[1].split("=")[1]
            instance_mem = instance_mem.strip('\n').strip('\t').strip(' ')
            outfile.write( instance_num+" "+str(to_mega(instance_mem))+"\n")

outfile.close()
