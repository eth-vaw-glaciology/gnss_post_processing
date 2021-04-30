# VAW GNSS Data Post Processing 📡 🛰️ 🏔️
Post processing of GNSS data recorded with VAW's Emlid and PPM GNSS receivers.

## Documentation:

### 0. DOWNLOAD DATA from Emlid receivers
For a semi-automatic download you need a device with a terminal and a browser that includes a developer environment.
0.0. CONNECT your device to the WiFi of the rover (password: emlidreach).
0.1. OPEN a web browser and enter "reach-rover<XX>.local" in the address line. (<XX> must be replaced by the number of the rover, eg. 01). The GUI of the rover you are connected to opens.
0.2. GO to the tab 'Logging' on the right side of the GUI.
0.3. OPEN the developer console in your browser (in Firefox Ctrl+Shift+K) and copy following in the command line:
```
document.body.appendChild(Object.assign(document.createElement('textarea'), {'value':'wget --content-disposition ' + [...document.getElementsByClassName('download-log-button')].map(a => a.href).join(' ')}))
```
A small textbox openens at the lower left of your browser window.
0.4. COPY&PASTE the text into a shell (Ctrl+Shift+V). The download of all files starts.

CHECKPOINT: All log files from the rover you connected to should be downloaded to your local device.

### 1. COPY your raw files from your receivers in subdirectories named by the receiver name (eg. 'rover00'), and put it in the directory 'raw_data'.

1.1 UNZIP the data (only for files from the Emlid receivers).
'cd' into the directory where your raw data files are.
```
>>> for z in *.zip; do unzip $z; done
```

CHECKPOINT: All of your raw data should be in the directory 'raw_data' in subdirectories named with the receiver name (eg. 'rover00').

### 2. RENAMING of file names (only for PPM receivers)
We have to rename the PPM receiver output files from a hexa-decimal time code to decimal time code.
'cd' into the subdirectory 'programs' of the directory where you found this README.txt file in.
```
>>> python rename_ppm_fname.py ../raw_data/<rover_name>
```

CHECKPOINT: The ppm raw files should now have names looking like YYYYmmddhhMM.gps

### 3. CONVERSION of raw files to RINEX
We convert the raw data into RINEX obs and nav files. These are neccessary for the post processing. In the following command you have to specify the directory with the files that you want to convert: <rover_name>, and the format of the raw data: <format>. The format can be either 'ubx' for Emlid receiver data, or 'nov' for PPM receiver data.
In this step also all obs and nav files within the <rover_name> directory are concatenated to a combined file each called '<rover_name>_comb.obs' and '<rover_name>_comb.nav'
```
>>> python conv2rnx.py ../raw_data/<rover_name> <format>
```

CHECKPOINT: In the <rover_name> directory you should find now several obs and nav files and also a combined obs and nav file called '<rover_name>_comb.obs' and '<rover_name>_comb.nav'

3.1 MANUAL CONCATENATION (!!!not neccessary!!!)
If you don't want to concatenate all files (maybe because of memory reasons), you can of course manually concatenate the files. It makes sense to have all files from your base station concatenated. Your rover files don't have to, but you might get continuity problems of your processing output between the files.
```
>>> cat conv_data/<rover_name>/*.obs > conv_data/<rover_name>/<rover_name>_comb.obs
>>> cat conv_data/<rover_name>/*.nav > conv_data/<rover_name>/<rover_name>_comb.nav
```

### 4. POSTPROCESSING with RTKLIB
This is the main part of GNSS postprocessing. This might take several minutes per recorded day, depending on the sampling frequency. All processing parameters are saved in the file 'setpar.conf'. You don't need to know, what every single parameter means. You can find a detailed explanation in the 'other/rtklib_manual.pdf'.
The standard way to run the postprocessing for one rover is:
```
>>> rnx2rtkp rover.obs base.obs base.nav -k setpar.conf
```
'rover.obs', 'base.obs' and 'base.nav' have to be replaced with the file pathes of the rover and base obs and nav files.
There are many options that can be chosen on top. Command line options precede options in the setpar.conf file.
```
>>> rnx2rtkp rover.obs base.obs base.nav -k setpar.conf -l <lon> <lat> <height> -p <mode> -o ../proc_data/<rover_name>/outputfile.pos
```

CHECKPOINT: In the directory proc data you should have the output .pos files. These are the final output files.

### 5. COORDINATE CONVERSION from WGS84 to LV95
The output of the GNSS postprocessing is in the WGS84 coordinate system. The python module 'pandas' has to be installed for this. The following command converts the output coordinates to the swiss LV95 system. (The keyword 'skiprows' in line 17 might need to be adjusted depending on the number of header lines. The number equals the number of header lines in the output.pos file not including the column label line.)
```
>>> python conv2LV95.py ../proc_data/<rover_name>/<rover_name>.pos
```

### 6. CHECKING
With the Jupyter Notebook 'gps_plot.ipynb' you can make quick plots of the processing output. To run the Jupyter Notebook, you need to have the modules 'pandas', and 'obspy' installed.
```
>>> jupyter notebook gps_plot.ipynb
```

### 7. VELOCITY CALCULATION
With the Jupyter Notebook 'calc_velocity.ipynb' you can calculate velocities from your post-processed GNSS data. It is setup to work best for the output of kinematically post-processed data. The output files are saved in the subdirectory 'final_data'.
```
>>> jupyter notebook calc_velocity.ipynb
```
