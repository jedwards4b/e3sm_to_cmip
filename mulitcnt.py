#!/usr/bin/env python

#PBS -A CESM0020
#PBS -N cmor_translate
#PBS -q main
#PBS -l walltime=08:00:00
#PBS -l select=1:ncpus=128:mpiprocs=1:ompthreads=128

import os
import subprocess
import multiprocessing
import re
import tempfile

import subprocess
from multiprocessing import Pool

def check_files(directory, varlist, masterdataroot, realm, period, expected_count=20):
    # Create a set of expected filenames based on your pattern (r1i, r2i, ..., r20i)
    expected_files = {f"r{i}i" for i in range(1, expected_count + 1)}
    
    # List actual files matching your naming pattern in the directory
    existing_files = set()
    pattern = re.compile(r"r(\d+)i")
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            match = pattern.search(filename)
            if match:
                existing_files.add(f"r{int(match.group(1))}i")
    
    # Identify missing files
    missing_files = expected_files - existing_files
    extra_files = existing_files - expected_files

    print(f"Directory: {directory}")
    print(f"Total files found matching pattern: {len(existing_files)}")


    if missing_files:
        print("Missing files:")
        yr = directory[102:106]
        for fname in sorted(missing_files, key=lambda x: int(re.findall(r'\d+', x)[0])):
            mbr = int(fname[1:-1]) + 10
            path = os.path.join(masterdataroot,f"b.e21.BSMYLE.f09_g17.{yr}-11.0{mbr}",realm,"proc","tseries",period)

            with tempfile.TemporaryDirectory(dir=os.environ["SCRATCH"]) as dname:
                source_path = os.path.join(masterdataroot, "CMIP6")
                target_path = os.path.join(dname, "CMIP6")
                os.symlink(source_path, target_path)
                        
                print(f" - {mbr} {yr} {path}")
                cmdargs = ["e3sm_to_cmip", "-v"," ".join(varlist), "-i", path ,"--realm",realm,
                        "-t","cmip6-cmor-tables/Tables/","-o",dname, "-u","dcpp_metadata.json", "--logdir","logs"]
                print(f"cmdargs is {cmdargs}")
                subprocess.run(cmdargs) 
    else:
        print("No missing files.")

    if extra_files:
        print("Extra files:")
        for fname in sorted(extra_files, key=lambda x: int(re.findall(r'\d+', x)[0])):
            print(f" - {fname}")
            
# Example Usage:

# Daily atm variables
#    varlist = ["tas", "tasmax", "tasmin", "sfcWind", "tdps", "clt", "psl"] 
# Monthly atm variables
#    varlist = ["rsdt", "rsut", "rlut", "rsutcs", "rlutcs", "rsds", "tauu", "tauv", "hfss", "hfls", "evspsbl", "pr", "tas", "tasmax", "tasmin", "sfcWind", "huss", "tdps", "clt", "ps", "psl" ] 
# Monthly land variables
#varlist = ["ts", "snld", "mrro", "cVeg", "cLitter", "gpp", "npp", "lai", "nbp", "rh", "ra"]
#varlist = ["pr", "rsds", "prhmax"]
# ^hourly 

masterdataroot="/glade/campaign/cesm/development/espwg/CESM2-DP/DCPP_submission/"

varlists = {}
periods = ("day_1", "hour_6", "month_1")
realms = ("atm", "lnd")

for period in periods:
    varlists[period] = {}
    for realm in realms:
        if realm == "atm":
            if period == "hour_6":
                varlists[period][realm] = ["uas", "vas", "psl", "pr"]
#            elif period == "day_1":
#                varlists[period][realm] = ["pr","prhmax", "rsds", "tas", "tasmax", "tasmin", "sfcWind", "tdps", "clt", "psl"]
#            elif period == "month_1":
#                varlists[period][realm] = ["rsdt", "rsut", "rlut", "rsutcs", "rlutcs", "rsds", "tauu", "tauv", "hfss", "hfls", "evspsbl", "pr", "tas", "tasmax", "tasmin", "sfcWind", "huss", "tdps", "clt", "ps", "psl" ] 
#        elif realm == "lnd":
#            if period == "month_1":
#                varlists[period][realm] = ["ts", "snld", "mrro", "cVeg", "cLitter", "gpp", "npp", "lai", "nbp", "rh", "ra"]
tasks = []
for period in periods:
    for realm in realms:
        if period in varlists.keys() and realm in (varlists[period]).keys():
            if period == "hour_6":
                pdir = "6hrLev"
            elif period == "day_1":
                pdir = "day"
            elif period == "month_1":
                if realm == "atm":
                    pdir = "Amon"
                else:
                    pdir = "Lmon"
            var = varlists[period][realm][0]
            for yr in range(2022, 2024):
                tasks.append([os.path.join(masterdataroot,"CMIP6","DCPP","NCAR","CESM2","dcppA-hindcast","s"+str(yr)+'-r1i1p1f1',pdir,var,"gn"),
                              varlists[period][realm], masterdataroot, realm, period])


with Pool(processes=16) as pool:
    results = pool.starmap(check_files, tasks)



