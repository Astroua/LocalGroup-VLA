
'''
Create a dirty for the given SPW

Should be run from the 13A-213_imaging folder on rubin
'''

import os
import sys
import numpy as np
from glob import glob
import socket

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, concat, split

# Load in the SPW dict in the repo on cedar
if socket.gethostname().lower() == 'segfault':
    execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/13A-213/spw_setup.py"))
else:
    execfile(os.path.expanduser("~/code/LocalGroup-VLA/13A-213/spw_setup.py"))

gal = str(sys.argv[-2])
spw_num = int(sys.argv[-1])

orig_dir = os.getcwd()

data_path = os.path.expanduser("~/space/ekoch/VLA_tracks/13A-213/")

os.chdir(os.path.join(data_path, gal, 'products'))

# The field name for WLM if "Wolf-Lundmark-"
if gal == "WLM":
    source = 'Wolf*'
else:
    source = '{}*'.format(gal)

# Output to test image within that galaxy's folder
if not os.path.exists("test_imaging"):
    os.mkdir("test_imaging")

output_path = "../test_imaging/spw_{}".format(spw_num)

if not os.path.exists(output_path):
    os.mkdir(output_path)

line_name = linespw_dict[gal][spw_num][0]
rest_freq = linespw_dict[gal][spw_num][1]

myvis = "{0}_13A-213_{1}_spw_{2}_LSRK.ms"\
    .format(gal, line_name, spw_num)

# The spw is now 0 in the concatenated MS
spw_num_concat = 0

# Grab the galaxy phasecentre
gal_props = galaxy_dict[gal.lower()]

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

if line_name == "HI":
    chan_width = 10
elif "OH" in line_name:
    chan_width = 5
else:
    chan_width = 3

# Don't image the channel edges
pad_chan = int(np.ceil(linespw_dict[gal][spw_num][2] * 0.05))
num_chan = int((linespw_dict[gal][spw_num][2] - 2 * pad_chan) / chan_width)

tclean(vis=myvis,
       datacolumn='data',
       imagename=os.path.join(output_path,
                              '{0}_13A-213_{1}_spw_{2}.dirty'
                              .format(gal, line_name, spw_num)),
       spw='0',
       field=source,
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=pad_chan,
       width=chan_width,
       nchan=num_chan,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=0,
       threshold='3.2mJy/beam',
       phasecenter=gal_props["phasecenter"],
       restfreq=rest_freq,
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

# os.chdir(orig_dir)
