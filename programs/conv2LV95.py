import sys
import os
from wgs84_ch1903 import GPSConverter
import numpy as np
import pandas as pd

"""Convert the WGS84 coordinates the output file from the RTKLIB processing into LV95 coordinates

.. rubric:: example
>>> python conv2LV95.py ../proc_data/rover01/rover1.pos
"""

def read_pos(filepath):
    """ Read .pos file into pandas dataframe 
    :param filepath: input filepath
    """
    df=pd.read_csv(filepath, skiprows=24, delim_whitespace=True, parse_dates=[['%', 'GPST']])
    df.rename(columns={'%_GPST':'time'}, inplace=True)
    df.set_index('time', inplace=True)
    return(df)

def conv2LV95(df):
    """ Converts lat/lon to LV95 
    :param df: dataframe with content of .pos file
    """
    lats = df['latitude(deg)'].tolist()
    longs = df['longitude(deg)'].tolist()
    heights = df['height(m)'].tolist()
    coords = zip(lats, longs, heights)
    conv=GPSConverter()
    #convert coordinates
    LV03_coords = np.array([conv.WGS84toLV03(lat, long, height) for lat, long, height in coords])
    #add constant for transformation from LV03 to LV95. 
    #!!!This transformation is not exact!!!
    LV95_east = np.array(LV03_coords)[:,0]+2e6
    LV95_north = np.array(LV03_coords)[:,1]+1e6
    LV95_height = np.array(LV03_coords)[:,2]
    
    df.insert(0, 'LV95_east', LV95_east)
    df.insert(1, 'LV95_north', LV95_north)
    df.insert(2, 'LV95_height', LV95_height)
    #df = df.applymap(lambda x: '{0:.3f}'.format(x))
 
    df.drop(['latitude(deg)', 'longitude(deg)', 'height(m)'], axis=1, inplace=True)
    return(df)

def save_pos(df, filepath):
    """Save dataframe with new coordinates to .csv file
    :param df: dataframe with converted coordinates
    :param filepath: input filepath
    """
    out_dir = os.path.dirname(filepath)
    in_file = os.path.basename(filepath)[:-4]
    out_file = in_file+'LV95.csv'
    df.to_csv(os.path.join(out_dir,out_file), sep=',', float_format='%.3f')
    return
    
if __name__=='__main__':
    filepath = sys.argv[1]
    df = read_pos(filepath)
    df = conv2LV95(df)
    save_pos(df, filepath)
