#!/usr/bin/python -w

import subprocess

def timestamp_to_secs(s):
	minsecs = s.rstrip("s").split('m')
	mins = int(minsecs[0])
	secmills = minsecs[1].split('.')
	return str(mins*60 + int(secmills[0])) + "." + secmills[1]

list_of_files = subprocess.Popen('ls ./test.job.o*', stdout=subprocess.PIPE, shell=True)
(output, err) = list_of_files.communicate()
output        = output.rstrip().split('\n')


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
		# open also test.job.eNUMBER to get overall timing
		with open("test.job.e"+instance_num, "r") as timefile:
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
				
		overall_time = float(tr) + float(tu) + float(ts)
		prepr_time = overall_time - float(soltime)
		print instance_name, num_variables, soltime, solscore, "|", \
		       str(overall_time), str(prepr_time)
