import glob
import os
import sys
import datetime

def rename_ppm_fname(in_dir):
    """ 
    Rename PPM files from hexa-decimal timestamp to decimal
    :param input/output directory

    .. rubric:: example
    >>> python rename_ppm_fname.py gps_work/raw_data/rover01
    """

    files = glob.glob(os.path.join(in_dir,'*'))

    for infile in files:
        try:
            source_file = os.path.basename(infile)
            source_dir = os.path.dirname(infile)
            hex_code = source_file[:-4] #hexadecimal code of file timestamp
            timestamp = int(hex_code,16) 
            date = datetime.datetime.fromtimestamp(timestamp) 
            new_datestr = date.strftime('%Y%m%d%H%M') #decimal time
            outfile = 'raw_'+new_datestr+'.gps' #Novatel OEMV6
            outfile = os.path.join(source_dir,outfile)
            os.rename(infile, outfile) #rename the files in decimal
        except ValueError:
            pass

if __name__=='__main__':
    in_dir = sys.argv[1]
    rename_ppm_fname(in_dir)
    print('Renaming of files successful.')
        
