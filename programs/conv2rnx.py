#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 11:01:20 2019
    
Convert u-blox or novatel raw files to rinex files
:param: in_dir: directory with raw files
:param: in_format: format of the in put raw files. Either 'ubx' or 'nov'.

.. rubric:: example
>>> python conv2rnx.py ../raw_data/rover01 ubx


@author: graeffd
"""
import glob
import os
import io
import sys
from functools import partial
import multiprocessing 


def raw2rnx(infile, in_format):
    rover_name = os.path.basename(os.path.dirname(infile))
    fname = rover_name+'_'+os.path.basename(infile)[4:-4]
    out_dir = os.path.join('../conv_data', rover_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    cmd = 'convbin -r '+in_format+' -d '+out_dir \
        +' -o '+fname+'.obs -n ' \
        +fname+'.nav -l ' \
        +fname+'.lnav -s ' \
        +fname+'.sbas ' \
        +infile #+' > /dev/null 2>&1' #prevents standard output
    os.system(cmd) #run rtklib command convbin
    return(out_dir)
    
def rm_not_needed(out_dir):
    lnav_files = glob.glob(os.path.join(out_dir,'*.lnav'))
    sbas_files = glob.glob(os.path.join(out_dir,'*.sbas'))
    for lnav, sbas in zip(lnav_files, sbas_files):
        try:
            os.remove(lnav)#only needen for rtklib V2.x
            os.remove(sbas)
        except:
            continue
    return

def get_raw_files(in_dir, in_format):
    if in_format=='ubx':
        extension = '.UBX'
    if in_format=='nov':
        extension = '.gps'
    infiles = glob.glob(os.path.join(in_dir,'*'+extension))
    return(infiles)

def run_gps_conv(infiles, in_format):
    for i, file in enumerate(infiles,1):
        out_dir = raw2rnx(file, in_format)
        rm_not_needed(out_dir)
    return(out_dir)

def cat_rnx(out_dir):
    #combines all rinex files in directory
    rover_name = os.path.basename(out_dir)
    cmd1 = 'cat '+os.path.join(out_dir,'*.obs')+' > '+os.path.join(out_dir,rover_name+'_comb.obs')
    cmd2 = 'cat '+os.path.join(out_dir,'*.nav')+' > '+os.path.join(out_dir,rover_name+'_comb.nav')
    os.system(cmd1)
    os.system(cmd2)
# =============================================================================
#     p = multiprocessing.Pool()
#     for i, out_dir in enumerate(p.imap(partial(raw2rnx, in_format=in_format), infiles),1):
#         rm_not_needed(out_dir)
#         sys.stdout.write('\r{} files of {} converted'.format(str(i), str(len(infiles))))
#         sys.stdout.flush()
#     p.close()
#     p.join()
# =============================================================================
    
if __name__=='__main__':
    in_dir = sys.argv[1]
    in_format = sys.argv[2]
    
    infiles = get_raw_files(in_dir, in_format)
    out_dir = run_gps_conv(infiles, in_format)
    cat_rnx(out_dir)
