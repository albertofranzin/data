#!/usr/bin/python -w

import subprocess
import sys
import re

orig_file      = sys.argv[1]
dir_to_compare = sys.argv[2]

# get output files
ls_command    = "ls "+dir_to_compare+"/test.job.o*"
list_of_files = subprocess.Popen(ls_command, stdout=subprocess.PIPE, shell=True)
(output, err) = list_of_files.communicate()
output        = output.rstrip().split('\n')

d = {}
with open("memory/memres.txt") as memf:
    for line in memf:
       (key, val) = line.split()
       d[int(key)] = val

with open("./shd/shd_mmhc.txt", "a") as tfile:
    for f in output:
        with open(f, "r") as resfile:
            mmpc_tu = ""
            mmpc_ts = ""
            mmpc_te = ""
            hc_tu   = ""
            hc_ts   = ""
            hc_te   = ""
            score   = ""
            net     = ""
            shd     = ""
            instance_num  = f.rstrip().split('.o')[-1]
            textfile = resfile.read().replace('\n','')
            instance_name = textfile.split("###############[1] \"Starting MMPC...\"")[0].replace('##################[1] ','').replace('"','').split('/')[1]
            print instance_name
            instance_text = textfile.split("###############[1] \"Starting MMPC...\"")[1]
            # if instance_text.count("")
            mmpc_time_textslice = instance_text.split("[1] \"MMPC done\"")[0].split("[1] \"MMPC TIME\"")[1].split(' ')
            mmpc_time_textslice = filter(None, mmpc_time_textslice)
            mmpc_tu = mmpc_time_textslice[3]
            mmpc_ts = mmpc_time_textslice[4]
            mmpc_te = mmpc_time_textslice[5]
            # print mmpc_tu, mmpc_ts, mmpc_te
            hc_time_textslice = instance_text.split("[1] \"creating indicator variables for edges...\"")[0].split("[1] \"HC TIME\"")[1].split(' ')
            hc_time_textslice = filter(None, hc_time_textslice)
            hc_tu = hc_time_textslice[3]
            hc_ts = hc_time_textslice[4]
            hc_te = hc_time_textslice[5]
            # print hc_tu, hc_ts, hc_te
            final_textslice = instance_text.split("final cost:")[1].split(' ')
            final_textslice = filter(None, final_textslice)
            score = final_textslice[0]
            net   = final_textslice[2]
            # print score, net
            r_command = "Rscript compute.shd.R 2 "+orig_file+" \""+net+"\""
            #print r_command
            r_out     =  subprocess.Popen(r_command, stdout=subprocess.PIPE, shell=True)
            (o2, e2)  = r_out.communicate()
            o         = o2.rstrip().split('\n')
            for rline in o:
                #print rline
                if re.match("SHD:",rline) != None:
                    shd = int(rline.rstrip('\n').strip(' ').strip('\t').split(':')[1])
            # print shd
            print score, shd, d[int(instance_num)]
            total_time = mmpc_tu+" | "+hc_tu+" | "+str(float(mmpc_tu)+float(hc_tu))
            tfile.write(instance_name+" | "+str(shd)+"\n")