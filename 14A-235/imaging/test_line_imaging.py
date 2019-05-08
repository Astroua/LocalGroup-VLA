
'''
Create a dirty for the given SPW

Should be run from the 14A-235_imaging folder on cedar
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

# Don't image the channel edges
pad_chan = int(np.ceil(linespw_dict[spw_num][2] * 0.05))
num_chan = int((linespw_dict[spw_num][2] - 2 * pad_chan) / chan_width[spw_num])

# Grab all of the MS tracks in the folder (should be 17)
myvis = "14A-235_lines.ms"

# Load in the SPW dict in the repo on cedar
execfile(os.path.expanduser("~/code/LocalGroup-VLA/14A-235/spw_setup.py"))

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

mypblimit = 0.1

for source in fourteenA_sources:

    casalog.post("Imaging {}".format(source))

    myimagesize = set_imagesize(myvis, spw_num, source, sample_factor=6.,
                                max_size=15000, pblevel=mypblimit)
    casalog.post("Image size: {}".format(myimagesize))

    # Image ALL channels in the MS. Just looking for reduction issues
    default('tclean')

    tclean(vis=myvis,
           datacolumn='corrected',
           imagename=os.path.join(output_path,
                                  '{0}_14A-235_{1}_spw_{2}.dirty'
                                  .format(source, linespw_dict[spw_num][0], spw_num)),
           spw=str(spw_num),
           field='{}*'.format(source),
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
           phasecenter=fourteenA_sources[source],
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
           parallel=True,
           )
