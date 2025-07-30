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

# complete list
varlist = ["abs550aer","abs550bc","abs550dust","abs550no3","abs550oa","abs550so4","abs550ss","airmass",
           "aoanh","bldep","c2h4","c2h5oh","c2h6","c3h6","c3h8","c4h10","ccn","ccn02","ccn1","cdnc",
           "cfc114","ch3coch3","ch3oh","ch4","ch4losssoil","cheaqpso4","chegph2oo1d","chegpso4",
           "chepasoa","chepnh4","chepno3","chepsoa","cltc","co","co2","cod","conccn","dms","do3chm",
           "drybc","drydust","dryh2","dryhno3","drynh3","drynh4","dryno3","drynoy","dryo3","dryoa",
           "dryso2","dryso4","dryss","e90inst","emiach4","emiaco","emianox","emiaoa","emiavnox",
           "emibbbc","emibbch4","emibbco","emibbdms","emibbnh3","emibbnox","emibboa","emibbso2",
           "emibbvoc","emibc","emibvoc","emic2h4","emic2h5oh","emic2h6","emic3h6","emic3h8","emic4h10",
           "emich3oh","emich4","emico","emidms","emidust","emih2","emiisop","emilkch4","emilnox",
           "eminh3","eminox","emioa","emiso2","emiso4","emiss","emivoc","h2","h2loss","h2o","h2prod",
           "hcfc22","hcho","hcl","hfc125","hfc134a","hno3","isop","jno2","lossch4","lossco","lossn2o",
           "lwp","meanage","mmraerh2o","mmrbc","mmrdust","mmrnh4","mmrno3","mmroa","mmrpm1","mmrpm10",
           "mmrpm2p5","mmrso4","mmrsoa","mmrss","n2o","nh50","no","no2","o3","o3inst","o3loss","o3prod",
           "o3ste","od443aer","od550aer","od550aerh2o","od550bb","od550bc","od550csaer","od550dust",
           "od550lt1aer","od550no3","od550oa","od550so4","od550soa","od550ss","od865aer","oh","pan",
           "pfull","phalf","photo1d","pod0","ptp","reffclwtop","rluscsaf","rlutaf","rlutch4ref","rlutcsaf",
           "rlutcsch4ref","rlutcso3ref","rluto3ref","rsutaf","rsutch4ref","rsutcsaf","rsutcsch4ref",
           "rsutcso3ref","rsuto3ref","so2","stratch4loss","tatp","tntrl","tntrs","toz","tropch4loss",
           "tropch4lossoh","tropdo3chm","tropo3ste","tropoz","ttop","ua","va","wa","wetbc","wetdust",
           "wethno3","wetnh3","wetnh4","wetno3","wetnoy","wetoa","wetso2","wetso4","wetss","zg","ztp"]
        
# List of successful
#varlist = ["evspbl", "od550aer", "od550dust", "ta"]

path="/glade/derecho/scratch/ccummins/CMOR_TESTING/f.e30_cam6_4_036.FLTHIST.ne30_L58.001/atm/tseries/"

cmd = ["/glade/work/cmip7/conda-envs/CMOR3.12/bin/e3sm_to_cmip", "-v"," ".join(varlist), "-i",path ,"--realm", "atm",
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
