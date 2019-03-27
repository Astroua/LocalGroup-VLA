
'''
Create a dirty for the given SPW

Should be run from the 13A-213_imaging folder on cedar

Stage 1 cleaning - clean to 5-sigma WITH auto-masking
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
gal_name = sys.argv[-2]

use_contsub = True if sys.argv[-1] == 'y' else False

spw_num = 0

if use_contsub:
    myvis = '13A-213_{}_spw0_LSRK.ms.contsub'.format(gal_name)
    output_path = "HI_stage1"
    imgname = '{0}_13A-213_{1}_spw_{2}.clean'.format(gal_name, "HI", spw_num)
else:
    myvis = '13A-213_{}_spw0_LSRK.ms'.format(gal_name)
    output_path = "HI_stage1_wcont"
    imgname = '{0}_13A-213_{1}_spw_{2}_wcont.clean'\
        .format(gal_name, "HI", spw_num)

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

# Initially clean to 5-sigma WITH automasking!

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
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
       deconvolver='multiscale',
       scales=[0, 5, 10, 50],  # Need to change b/w C+D vs D??
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=1000,  # Force a lot of major cycles
       usemask='auto-multithresh',
       mask=None,
       pbmask=0.1,
       minpercentchange=2.,
       noisethreshold=4.,
       lownoisethreshold=1.5,
       sidelobethreshold=2.,
       minbeamfrac=0.1,
       verbose=True,
       )
