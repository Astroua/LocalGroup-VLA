
'''
Create a dirty for the given SPW

Should be run from the 13A-213_imaging folder on cedar

Stage 1 cleaning - no clean mask down to 5-sigma
'''

import os
import sys

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, listobs

# Load in the info dicts from the repo
execfile(os.path.expanduser("~/code/LocalGroup-VLA/13A-213/spw_setup.py"))


# galaxy name given. And is folder name
gal_name = sys.argv[-1]

myvis = '13A-213_{}_spw0_LSRK.ms.contsub'.format(gal_name)
spw_num = 0

output_path = "HI_stage1"

if not os.path.exists(output_path):
    os.mkdir(output_path)

# List the obs in the MS
listobs(myvis)

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

# Choose something low as there is some HI near the edges of the mosaic
mypblimit = 0.05

# Set to something fairly large.
# My routine is underestimating the pb limit size a bit
# for some of these cases
myimagesize = 1024
# myimagesize = set_imagesize(myvis, spw_num, source, sample_factor=6.,
#                             max_size=15000, pblevel=mypblimit)
casalog.post("Image size: {}".format(myimagesize))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

# Don't image the channel edges
# pad_chan = int(np.ceil(linespw_dict[spw_num][2] * 0.05))
# num_chan = int(linespw_dict[spw_num][2]) - 2 * pad_chan

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path,
                              '{0}_13A-213_{1}_spw_{2}.clean'
                              .format(gal_name, "HI", spw_num)),
       spw=str(spw_num),
       field='*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=galaxy_dict[gal_name.lower()]['HI_start'],
       width=1,
       nchan=galaxy_dict[gal_name.lower()]['HI_nchan'],
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=1000000,
       threshold='',
       nsigma=5.,
       phasecenter=galaxy_dict[gal_name.lower()]['phasecenter'],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       usemask='pb',
       mask=None,
       deconvolver='multiscale',
       scales=[0, 5, 10, 50],  # Need to change b/w C+D vs D??
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=1000,  # Force a lot of major cycles
       )
