
'''
Create a dirty for the given SPW

Should be run from the 13A-213_imaging folder on rubin
'''

import os
import sys
import numpy as np
from glob import glob

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, virtualconcat, split

data_folder = sys.argv[-2]
spw_num = int(sys.argv[-1])

orig_dir = os.getcwd()

os.chdir(data_folder)

# The field name for WLM if "Wolf-Lundmark-"
if data_folder == "WLM":
    source = 'Wolf*'
else:
    source = '{}*'.format(data_folder)

# Output to test image within that galaxy's folder
if not os.path.exists("test_imaging"):
    os.mkdir("test_imaging")

output_path = "test_imaging/spw_{}".format(spw_num)

if not os.path.exists(output_path):
    os.mkdir(output_path)

# Check if the concatenated SPW already exists
concat_vis = "13A-213_{0}_spw{1}.ms".format(data_folder, spw_num)

if not os.path.exists(concat_vis):

    # Grab all of the MS tracks in the folder
    # Need to look for each track in the calibrated folder
    # for spectral lines
    track_folders = glob("calibrated/13A-213*_speclines")

    print("Track folder: {}".format(track_folders))

    myviss = []

    for fol in track_folders:

        # Look for calibrated track
        vis_track = glob(os.path.join(fol, "13A-213*speclines.ms"))
        if len(vis_track) == 0:
            raise ValueError("Cannot find MS in track {}".
                             format(fol.split("/")[-1]))
        if len(vis_track) > 1:
            raise ValueError("Found multiple MS in track {}".
                             format(fol.split("/")[-1]))

        vis_track = vis_track[0]

        # Split out the SPW from that MS
        default("split")
        output_name = "{0}_spw{1}.ms".format(vis_track.rstrip(".ms"), spw_num)
        split(vis=vis_track, outputvis=output_name, spw=str(spw_num),
              datacolumn='corrected', field=source)


        myviss.append(output_name)

    if len(myviss) == 0:
        raise ValueError("Found no tracks.")

    # Concatenate corrected data column for that SPW
    virtualconcat(vis=myviss, concatvis=concat_vis)

myvis = concat_vis

# The spw is now 0 in the concatenated MS
spw_num_concat = 0

# Load in the SPW dict in the repo
execfile(os.path.expanduser("~/LocalGroup-VLA/13A-213/spw_setup.py"))
# Grab the galaxy phasecentre
gal_props = galaxy_dict[data_folder.lower()]

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num_concat, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

mypblimit = 0.1

myimagesize = set_imagesize(myvis, spw_num_concat, source, sample_factor=6.,
                            max_size=15000, pblevel=mypblimit)
casalog.post("Image size: {}".format(myimagesize))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

# Don't image the channel edges
pad_chan = int(np.ceil(linespw_dict[spw_num][2] * 0.05))
num_chan = int(linespw_dict[spw_num][2]) - 2 * pad_chan

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path,
                              '{0}_13A-213_{1}_spw_{2}.dirty'
                              .format(data_folder, linespw_dict[spw_num][0], spw_num)),
       spw=str(spw_num_concat),
       field=source,
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=pad_chan,
       width=1,
       nchan=num_chan,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=0,
       threshold='3.2mJy/beam',
       phasecenter=gal_props["phasecenter"],
       restfreq=linespw_dict[spw_num][1],
       outframe='LSRK',
       pblimit=mypblimit,
       usemask='pb',
       mask=None,
       deconvolver='hogbom',
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=False,
       parallel=False,
       # parallel=True,
       )

os.chdir(orig_dir)
