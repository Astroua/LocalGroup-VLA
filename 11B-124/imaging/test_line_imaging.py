
'''
Create a dirty for the given SPW

Should be run from the 17B-162_imaging folder on cedar
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

# Grab all of the MS tracks in the folder (should be 17)
myvis = "11B-124_lines.ms"

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

mypblimit = 0.1

# Will look for all M33 fields and assume they are all used in the mosaic
source = 'M31'

myimagesize = set_imagesize(myvis, spw_num, source, sample_factor=6.,
                            max_size=15000, pblevel=mypblimit)
casalog.post("Image size: {}".format(myimagesize))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

# Don't image the channel edges
# pad_chan = int(np.ceil(linespw_dict[spw_num][2] * 0.05))
# num_chan = int(linespw_dict[spw_num][2]) - 2 * pad_chan

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path,
                              'M31_11B-124_{0}_spw_{1}.dirty'
                              .format("HI", spw_num)),
       spw=str(spw_num),
       field='M33*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=1,
       width=1,
       nchan=-1,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=0,
       threshold='3.2mJy/beam',
       phasecenter='J2000 00h42m44.350 +41d16m08.63',
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       usemask='pb',
       mask=None,
       deconvolver='hogbom',
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=False,
       parallel=True,
       )
