
import os

from tasks import tclean

myvis = '12A-304_lines_Ctracks.ms'

# Scale from 14A-235 D-config mosaic
myimagesize = [4500, 5000]

mycellsize = '3arcsec'

mypblimit = 0.05

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join('test_imaging',
                              'M31_12A-304_Ctracks_HI.dirty'),
       spw='0',
       field='M31*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start='-600km/s',
       width='10km/s',
       nchan=56,
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
       # parallel=True,
       parallel=False,
       )

# Some poor phase solutions in there... will need to go back to flagging

# Try the B-array. NOTE: this is a BIG image.

myvis = '12A-304_lines_Btracks.ms'

# Scale from 14A-235 D-config mosaic
myimagesize = [13500, 15000]

mycellsize = '1arcsec'

mypblimit = 0.05

tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join('test_imaging',
                              'M31_12A-304_Btracks_HI.dirty'),
       spw='0',
       field='M31*',
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start='-600km/s',
       width='10km/s',
       nchan=56,
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
       # parallel=True,
       parallel=False,
       )
