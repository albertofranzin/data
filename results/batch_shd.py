#!/usr/bin/python -w

import subprocess
import sys
import re

instance_name  = sys.argv[1]
dir_to_compare = sys.argv[2]

ls_command    = "ls "+dir_to_compare+"/test.job.o*"
list_of_files = subprocess.Popen(ls_command, stdout=subprocess.PIPE, shell=True)
(output, err) = list_of_files.communicate()
output        = output.rstrip().split('\n')

for f in output:
    with open(f, "r") as resfile:
        lines = resfile.readlines()
        found = False
        for line in lines:
            mat = re.match("net:", line)
            if mat != None:
                found = True
                lis = line.rstrip('\n').strip(' ').strip('\t').split(":")
                #print lis
                factors = lis[1].strip('\t').strip(' ').replace('[','(').replace(']',')')
                #print factors
                r_command = "Rscript compute.shd.R 2 "+instance_name+".mat \""+factors+"\""
                #print r_command
                r_out     =  subprocess.Popen(r_command, stdout=subprocess.PIPE, shell=True)
                (o2, e2)  = r_out.communicate()
                o         = o2.rstrip().split('\n')
                for rline in o:
                    #print rline
                    if re.match("SHD:",rline) != None:
                        print rline.rstrip('\n').strip(' ').strip('\t').split(':')[1]
        if found == False:
            print "-"

