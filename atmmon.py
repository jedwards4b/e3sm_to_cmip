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
varlist = ["rsdt", "rsut", "rlut", "rsutcs", "rlutcs", "rsds", "tauu", "tauv", "hfss", "hfls", "evspsbl", "pr", "tas", "tasmax", "tasmin", "sfcWind", "huss", "tdps", "clt", "ps", "psl" ] 
for path in glob.iglob(dataroot + "*/atm/proc/tseries/month_1/"):
    if "195" in path:
        continue
    yr = path[85:89]
    member = int(path[93:96]) - 10
    dolist = []
    
    for var in varlist:
        if glob.glob(dataroot+"CMIP6/DCPP/NCAR/CESM2/dcppA-hindcast/s"+yr+"*/Amon/"+var+"/gn/"+var+"_Amon_CESM2_dcppA-hindcast_s"+yr+"-r"+str(member)+"*.nc"):
#            print(f"Removing {var} from list")
            continue
        else:
            dolist.append(var)
    if len(dolist) > 0:
        print(f"yr is {yr} member is {member}, list is:" + " ".join(dolist))
        subprocess.run(["e3sm_to_cmip", "-v"," ".join(dolist), "-i", path ,"--realm","atm",
                    "-t","cmip6-cmor-tables/Tables/","-o",dataroot, "-u","dcpp_metadata.json", "--logdir","logs"])
