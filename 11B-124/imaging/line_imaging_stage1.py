
'''
Create a dirty for the given SPW

Should be run from the M31_imaging/11B-124 folder on cedar

Stage 1 cleaning - no clean mask down to 5-sigma
'''

import os

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, listobs

spw_num = 0

output_path = "HI_stage1"

if not os.path.exists(output_path):
    os.mkdir(output_path)

# Grab all of the MS tracks in the folder (should be 17)
myvis = "11B-124_HI_spw_0_LSRK.ms.contsub"

# Run listobs
listobs(vis=myvis)

# Assume we can set reasonable image parameters from any of the tracks
mycellsize = set_cellsize(myvis, spw_num, sample_factor=6.,
                          baseline_percentile=95,
                          return_type="str")
casalog.post("Cell size: {}".format(mycellsize))

# Choose something low as there is some HI near the edges of the mosaic
mypblimit = 0.05

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

image_name = os.path.join(output_path,
                          'M31_11B-124_{0}_spw_{1}.clean'
                          .format("HI", spw_num))

if os.path.exists("{}.image".format(image_name)):
    # Need to delete the old mask to use auto masking
    os.system("rm -rf {}.mask".format(image_name))
    calcres = False
    calcpsf = False
    nsigma = 2.
    cycleniter = 2000
    usemask = 'auto-multithresh'
else:
    calcres = True
    calcpsf = True
    nsigma = 5.
    cycleniter = 1000
    usemask = 'pb'

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=image_name,
       spw=str(spw_num),
       field='M31*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=16,
       width=1,
       nchan=1074,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=1000000,
       threshold='',
       nsigma=nsigma,
       phasecenter='J2000 00h42m44.350 +41d16m08.63',
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       usemask=usemask,
       mask=None,
       deconvolver='multiscale',
       scales=[0, 5, 10, 50],
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=cycleniter,  # Force a lot of major cycles
       calcres=calcres,
       calcpsf=calcpsf,
       minpercentchange=2.,  # Auto-mask settings for stage 2
       noisethreshold=3.,
       lownoisethreshold=1.5,
       pbmask=0.05,
       sidelobethreshold=2.,
       minbeamfrac=0.1,
       )
