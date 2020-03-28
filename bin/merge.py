#!/usr/bin/env python

import os,sys

num_args = len(sys.argv)
run_dir = os.getcwd()
workflow_stage = sys.argv[1]
filter_var = str(sys.argv[2])

out_file = "%s/results_%d_%s.txt" % (run_dir,workflow_stage,filter_var)

with open(out_file,'w') as output:
    for i in range(3,num_args):
        with open(str(sys.argv[i]),'r') as in_file:
            for line in in_file:
                output.write(line)
