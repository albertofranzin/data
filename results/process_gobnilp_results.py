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

# get adjacency matrices
ls_matrices  = "ls "+dir_to_compare+"/*.out"
list_of_mats = subprocess.Popen(ls_matrices, stdout=subprocess.PIPE, shell=True)
(out_m, e_m) = list_of_mats.communicate()
out_m        = out_m.rstrip().split('\n')

d = {}
with open("memory/memres.txt") as memf:
    for line in memf:
       (key, val) = line.split()
       d[int(key)] = val

memfile = open("memory_results.txt", "a")

for f in output:
    with open(f, "r") as resfile:
        instance_num = f.rstrip().split('.o')[-1] # extract job number
        instance_name = ""
        num_variables = 0
        soltime = ""
        solscore = ""
        tr = ""
        tu = ""
        ts = ""
        shd = ""
        prepr_time = ""
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
        lines = resfile.readlines()
        for line in lines:
            lineitems = line.rstrip('\n').split(' ')
            # print lineitems
            # I only need to extract some relevant information
            # everything else may be discarded
            # I do this in the not-so-efficient-but-veeerrry-simple way
            if len(lineitems) > 4 and lineitems[0] == "presolved" \
                                  and lineitems[1] == "problem" \
                                  and lineitems[2] == "has" \
                                  and lineitems[4] == "variables":
                num_variables = int(lineitems[3])
            elif len(lineitems)  > 3 and lineitems[0] == "Solving" \
                                     and lineitems[1] == "Time" \
                                     and lineitems[2] == "(sec)" \
                                     and lineitems[3] == ":":
                soltime = lineitems[4]
            elif len(lineitems) == 4 and lineitems[0] == "BN" \
                                     and lineitems[1] == "score" \
                                     and lineitems[2] == "is":
                solscore = lineitems[3]
            elif len(lineitems) == 2 and lineitems[0] == "Problem" \
                                     and lineitems[1].split('\t')[0] == "name:":
                instance_name = lineitems[1].split('\t')[2].split('.')[0]

        #print dir_to_compare+"/"+instance_name+".gob.out"
        if out_m.count(dir_to_compare+"/"+instance_name+".gob.out") > 0:
            r_command = "Rscript compute.shd.R 1 "+orig_file+" "+dir_to_compare+"/"+instance_name+".gob.out"
            #print r_command
            r_out     =  subprocess.Popen(r_command, stdout=subprocess.PIPE, shell=True)
            (o2, e2)  = r_out.communicate()
            o         = o2.rstrip().split('\n')
            for rline in o:
                #print rline
                if re.match("SHD:",rline) != None:
                    shd = int(rline.rstrip('\n').strip(' ').strip('\t').split(':')[1])
                
        overall_time = float(tr) + float(tu) + float(ts)
        if soltime != "":
            prepr_time = overall_time - float(soltime)
        print instance_name, num_variables, soltime, solscore, "|", \
               str(overall_time), str(prepr_time), "|", str(shd), d[int(instance_num)]
        memfile.write(instance_name+" "+str(d[int(instance_num)])+"\n")

memfile.close()