
'''
Create a dirty for the given SPW

Should be run from the 15A-175 folder on cedar
'''

import os
import sys
import numpy as np

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean

spw_num = int(sys.argv[-1])

output_path = "spw_{}".format(spw_num)

if not os.path.exists(output_path):
    os.mkdir(output_path)

# Set channel widths to make dirty cubes with
chan_width = {0: 10, 1: 5, 2: 5, 3: 5, 4: 5}

# Load in the SPW dict in the repo on cedar
# execfile(os.path.expanduser("~/code/LocalGroup-VLA/15A-175/spw_setup.py"))
execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/15A-175/spw_setup.py"))

# Don't image the channel edges
pad_chan = int(np.ceil(linespw_dict[spw_num][2] * 0.05))
num_chan = int((linespw_dict[spw_num][2] - 2 * pad_chan) / chan_width[spw_num])

# Grab all of the MS tracks in the folder (should be 17)
myvis = "15A-175_Btracks_lines.ms"

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

mypblimit = 0.1

source = 'M31'

casalog.post("Imaging {}".format(source))

myimagesize = set_imagesize(myvis, spw_num, source, sample_factor=6.,
                            max_size=15000, pblevel=mypblimit)
casalog.post("Image size: {}".format(myimagesize))

# Check to see if the images already exist. If so, continue
out_name = os.path.join(output_path,
                        'M31_15A-175_Btracks_{0}_spw_{1}.dirty'
                        .format(linespw_dict[spw_num][0], spw_num))

# if os.path.exists("{}.residual".format(out_name)):
#     casalog.post("Already found image products for {}. Skipping.".format(source))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=out_name,
       spw=str(spw_num),
       field='M31*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=pad_chan,
       width=chan_width[spw_num],
       nchan=num_chan,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=0,
       threshold='3.2mJy/beam',
       phasecenter="J2000 00h44m33.854 +41d57m42.572",
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
       # parallel=True,
       parallel=False,
       )
