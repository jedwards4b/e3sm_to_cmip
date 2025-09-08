#!/usr/bin/env python

#PBS -A CESM0024
#PBS -N cmor_translate
#PBS -q main
#PBS -l walltime=08:00:00
#PBS -l select=1:ncpus=128:mpiprocs=1:ompthreads=128

import os
import glob
import subprocess

dataroot=os.getenv("SCRATCH")
varlist = ["evspsblsoi", "lai", "mrfso", "mrro", "mrros", "mrso", "mrsos", ]
path="/glade/derecho/scratch/cmip7/archive/timeseries/b.e30_beta06.B1850C_LTso.ne30_t232_wgx3.192.wrkflw.1_32/lnd/hist"

cmd = ["/glade/work/cmip7/conda-envs/CMOR/bin/e3sm_to_cmip", "-v"," ".join(varlist), "-i",path ,"--realm", "lnd",
       "-t","cmip6-cmor-tables/Tables/","-o", dataroot, "-u","cmip7Amon_metadata.json", "--logdir", "logs"]
print(f"running {cmd}")
subprocess.run(cmd)


#for var in varlist:
#    try:
#        cmd = ["/glade/work/cmip7/conda-envs/CMOR3.12/bin/e3sm_to_cmip", "-v",var, "-i",path ,"--realm", "atm",
#                        "-t","cmip6-cmor-tables/Tables/","-o", dataroot, "-u","cmip7Amon_metadata.json", "--logdir", "logs"]
#        print(f"running {cmd}")
#        subprocess.run(cmd)
#        
#    except subprocess.CalledProcessError as e:
#        print(f"Error executing command: {e}")
#        print(f"Stderr: {e.stderr}")
