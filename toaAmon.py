#!/usr/bin/env python

#PBS -A CESM0020
#PBS -N cmor_translate
#PBS -q main
#PBS -l walltime=08:00:00
#PBS -l select=1:ncpus=128:mpiprocs=1:ompthreads=128

import os
import glob
import subprocess

dataroot="/glade/campaign/cesm/development/espwg/CESM2-DP/DCPP_submission/"
for path in glob.iglob(dataroot + "*/atm/proc/tseries/month_1/"):
    if "195" in path:
        continue
    subprocess.run(["e3sm_to_cmip", "-v","rsdt rsut rlut rsutcs rlutcs ", "-i", path ,"--realm","atm",
                    "-t","cmip6-cmor-tables/Tables/","-o",dataroot, "-u","dcpp_metadata.json", "--logdir","logs"])
