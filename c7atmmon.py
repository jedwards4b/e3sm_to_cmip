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
varlist = ["aod550volso4","ccb","cct","cfc113global","cfc11global","cfc12global","ch4","ch4Clim","ch4global","ch4globalClim",
           "ci","cl","cli","clivi","clt","clw","clwvi","co2","co2Clim","co2mass","co2massCLim","evspsbl","fco2antt","fco2fos",
           "fco2nat","hcfc22global","hfls","hfss","hur","hurs","hus","huss","mc","n2o","n2oClim","n2oglobal","n2oglobalClim",
           "o3","o3Clim","pfull","phalf","pr","prc","prra","prsn","prw","ps","psl","rlds","rldscs","rlus","rluscs","rlut",
           "rlutcs","rsds","rsdscs","rsdt","rsus","rsuscs","rsut","rsutcs","rtmt","sbl","sci","sfcWind","ta","tas",
           "tasmax","tasmin","tauu","tauv","ts","ua","uas","va","vas","wap","zg"]
path="/glade/derecho/scratch/cmip7/archive/timeseries/b.e30_beta06.B1850C_LTso.ne30_t232_wgx3.192.wrkflw.1_32/atm/hist"

cmd = ["/glade/work/cmip7/conda-envs/CMOR/bin/e3sm_to_cmip", "-v"," ".join(varlist), "-i",path ,"--realm", "atm",
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
