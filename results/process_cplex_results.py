#!/usr/bin/python -w

import subprocess
import sys
import re

def timestamp_to_secs(s):
    minsecs = s.rstrip("s").split('m')
    mins = int(minsecs[0])
    secmills = minsecs[1].split('.')
    return str(mins*60 + int(secmills[0])) + "." + secmills[1]

orig_file      = sys.argv[1]
dir_to_compare = sys.argv[2]

# get output files
ls_command    = "ls "+dir_to_compare+"/test.job.o*"
list_of_files = subprocess.Popen(ls_command, stdout=subprocess.PIPE, shell=True)
(output, err) = list_of_files.communicate()
output        = output.rstrip().split('\n')


for f in output:
    with open(f, "r") as resfile:
        textfile = resfile.read().replace('\n','')
        instance_name = textfile.split("###############[1] \"Starting MMPC...\"")[0].replace('##################[1] ','').replace('"','').split('/')[1]
        # print instance_name
        score   = ""
        net     = ""
        shd     = ""
        cplex_time = ""
        instance_num  = f.rstrip().split('.o')[-1] # extract job number
        instance_name = ""
        num_variables = 0
        soltime = ""
        solscore = ""
        tr = ""
        tu = ""
        ts = ""
        # open also test.job.eNUMBER to get overall timing
        with open(dir_to_compare+"/test.job.e"+instance_num, "r") as timefile:
            tlines = timefile.readlines()
            for tline in tlines:
                tli = tline.rstrip('\n').split('\t')
                if tli[0] == "real":
                    tr = timestamp_to_secs(tli[1])
                elif tli[0] == "user":
                    tu = timestamp_to_secs(tli[1])
                elif tli[0] == "sys":
                    ts = timestamp_to_secs(tli[1])
        instance_text = textfile.split("###############[1] \"Starting MMPC...\"")[1]
        interesting_textslice = instance_text.split("Total (root+branch&cut) = ")[1]
        # print interesting_textslice
        cplex_time = float(interesting_textslice.split('sec')[0])
        score      = float(interesting_textslice.split('cost:')[1].split('-----')[0])
        net        = interesting_textslice.split('net:')[1].strip(' ').replace('[','(').replace(']',')')
        nodes      = int(interesting_textslice.split('# nodes:')[1].split('#')[0])
        cpcs_vars  = int(interesting_textslice.split('# cpcs vars:')[1].split('#')[0])
        edge_vars  = int(interesting_textslice.split('# edge vars:')[1].split('net')[0])
        r_command = "Rscript compute.shd.R 2 "+orig_file+" \""+net+"\""
        #print r_command
        r_out     =  subprocess.Popen(r_command, stdout=subprocess.PIPE, shell=True)
        (o2, e2)  = r_out.communicate()
        o         = o2.rstrip().split('\n')
        for rline in o:
            #print rline
            if re.match("SHD:",rline) != None:
                shd = int(rline.rstrip('\n').strip(' ').strip('\t').split(':')[1])
        print cplex_time, score, nodes, cpcs_vars, edge_vars, shd, tr, tu, ts
