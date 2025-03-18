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
varlist = ["ts", "snld", "mrro", "cVeg", "cLitter", "gpp", "npp", "lai", "nbp", "rh", "ra"] 
for path in glob.iglob(dataroot + "*/lnd/proc/tseries/month_1/"):
    if "195" in path:
        continue
    yr = path[85:89]
    member = int(path[93:96]) - 10
    dolist = []
    
    for var in varlist:
        if glob.glob(dataroot+"CMIP6/DCPP/NCAR/CESM2/dcppA-hindcast/s"+yr+"*/Lmon/"+var+"/gn/v20250318/"+var+"_Lmon_CESM2_dcppA-hindcast_s"+yr+"-r"+str(member)+"*.nc"):
#            print(f"Removing {var} from list")
            continue
        else:
            dolist.append(var)
    print(f"yr is {yr} member is {member}, list is:" + " ".join(dolist))
    subprocess.run(["e3sm_to_cmip", "-v"," ".join(dolist), "-i", path ,"--realm","lnd",
                    "-t","cmip6-cmor-tables/Tables/","-o",dataroot, "-u","dcpp_metadata.json", "--logdir","logs"])
