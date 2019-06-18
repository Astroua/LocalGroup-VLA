
'''
Should be run from the 14A-235 folder on cedar or SegFault

Meant for imaging NGC 185 and 205. The M31 cube is much much
larger with more complex emission.

Stage 1 cleaning - clean to 5-sigma WITH auto-masking
Also creates a copy of the dirty residual cube

To be run in CASA 5.5

'''

import os
import sys
import socket
import numpy as np

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, listobs

# Load in the info dicts from the repo
host_name = socket.gethostname()
if host_name == 'segfault':
    execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/14A-235/spw_setup.py"))
elif 'cedar' in host_name:
    execfile(os.path.expanduser("~/code/LocalGroup-VLA/14A-235/spw_setup.py"))
else:
    raise ValueError("Not running on SegFault or cedar? Unsure where the code repo is.")

# galaxy name given. And is folder name
gal_name = sys.argv[-3]

assert gal_name in fourteenA_sources.keys()

if gal_name == "M31":
    raise NotImplementedError("Do no use this script to image M31!")

use_contsub = True if sys.argv[-2] == 'y' else False

# Number of channels to use for each channel in the output cube
chan_width = int(sys.argv[-1])

spw_num = 0

if use_contsub:
    myvis = '{}_14A-235_HI_spw_0_LSRK.ms.contsub'.format(gal_name)
    output_path = "{0}_HI_imaging_chanwidth_{1}".format(gal_name, chan_width)
    imgname = '{0}_14A-235_{1}_spw_{2}.clean'.format(gal_name, "HI", spw_num)
else:
    myvis = '{}_14A-235_HI_spw_0_LSRK.ms'.format(gal_name)
    output_path = "{0}_HI_imaging_wcont_chanwidth_{1}".format(gal_name, chan_width)
    imgname = '{0}_14A-235_{1}_spw_{2}_wcont.clean'\
        .format(gal_name, "HI", spw_num)

if not os.path.exists(output_path):
    os.mkdir(output_path)

# List the obs in the MS
listobs(myvis)

# Assume we can set reasonable image parameters from any of the tracks
# mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
#                           baseline_percentile=95,
#                           return_type="str")
mycellsize = '9.3arcsec'
casalog.post("Cell size: {}".format(mycellsize))

# Choose something low as there is some HI near the edges of the mosaic
mypblimit = 0.05
# mypblimit = 0.15

# Set to something fairly large.
# myimagesize = set_imagesize(myvis, spw_num, gal_name, sample_factor=6.,
#                             max_size=15000, pblevel=mypblimit)
myimagesize = 512
casalog.post("Image size: {}".format(myimagesize))

# Calculate number of channels based on the width
# Round up for fractions
nchans = int(np.ceil((fourteenA_HI_channels[gal_name]['end'] - fourteenA_HI_channels[gal_name]['start']) / chan_width))

casalog.post("Number of channels: {}".format(nchans))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

# Make a dirty cube

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
       spw=str(spw_num),
       field='{}*'.format(gal_name),
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=fourteenA_HI_channels[gal_name]['start'],
       width=chan_width,
       nchan=nchans,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=0,
       threshold='',
       nsigma=5.,
       phasecenter=fourteenA_sources[gal_name],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       deconvolver='multiscale',
       scales=[0, 5, 10, 50],  # Need to change b/w C+D vs D??
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=False,
       parallel=True,
       cycleniter=1000,  # Force a lot of major cycles
       usemask='auto-multithresh',
       mask=None,
       pbmask=0.1,
       verbose=True,
       )

# Copy the dirty residual into its own directory
dirty_cube_path = os.path.join(output_path, "dirty_cube")

if not os.path.exists(dirty_cube_path):
    os.mkdir(dirty_cube_path)

os.system("cp -r {0}.residual {1}".format(os.path.join(output_path, imgname),
                                          dirty_cube_path))

# Initially clean to 5-sigma WITH automasking!

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
       spw=str(spw_num),
       field='{}*'.format(gal_name),
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=fourteenA_HI_channels[gal_name]['start'],
       width=1,
       nchan=nchans,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=1800,
       threshold='20.0mJy/beam',
       # nsigma=5.,
       phasecenter=fourteenA_sources[gal_name],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       deconvolver='multiscale',
       scales=[0, 6, 12, 24, 80],
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=600,  # Force a lot of major cycles
       usemask='auto-multithresh',
       mask=None,
       pbmask=mypblimit,
       minpercentchange=2.,
       noisethreshold=4.,
       lownoisethreshold=2.,
       sidelobethreshold=2.,
       minbeamfrac=0.1,
       verbose=True,
       calcres=False,
       calcpsf=False,
       # fastnoise=False,  # Use noise calc more robust for extended emission
       )

orig_stage1_path = os.path.join(output_path, "HI_stage1_orig")

if not os.path.exists(orig_stage1_path):
    os.mkdir(orig_stage1_path)

os.system("cp -r {0}.residual {1}".format(os.path.join(output_path, imgname),
                                          orig_stage1_path))
os.system("cp -r {0}.image {1}".format(os.path.join(output_path, imgname),
                                       orig_stage1_path))
os.system("cp -r {0}.model {1}".format(os.path.join(output_path, imgname),
                                       orig_stage1_path))


# Finally clean down to 2-sigma
# Limit larger scales for msclean

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
       spw=str(spw_num),
       field='{}*'.format(gal_name),
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=fourteenA_HI_channels[gal_name]['start'],
       width=1,
       nchan=nchans,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=1000000,
       threshold='5mJy/beam',
       # nsigma=3.,
       phasecenter=fourteenA_sources[gal_name],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       deconvolver='multiscale',
       scales=[0, 6, 12],
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=10000,
       usemask='auto-multithresh',
       mask=None,
       pbmask=mypblimit,
       minpercentchange=2.,
       noisethreshold=4.,
       lownoisethreshold=1.5,
       sidelobethreshold=2.,
       minbeamfrac=0.1,
       verbose=True,
       calcres=False,
       calcpsf=False,
       # fastnoise=False,  # Use noise calc more robust for extended emission
       )
