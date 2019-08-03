
'''
Combine the tracks, then split out the science fields
'''

import os
import sys
from glob import glob

from tasks import concat, mstransform

# Grab all of the MS tracks in the folder
# Btracks
myvis = glob("orig_ms/Btracks/*.ms")

assert len(myvis) == 16

default('concat')
concat(vis=myvis, concatvis='12A-304_lines_Btracks_all.ms')

default('mstransform')
mstransform(vis='12A-304_lines_Btracks_all.ms',
            outputvis='12A-304_lines_Btracks.ms',
            field='M31*',
            datacolumn='corrected',
            spw='',
            mode='channel',
            start=1,
            nchan=-1,
            width=1,
            combinespws=True,
            regridms=True,
            keepflags=False)

# Ctracks
myvis = glob("orig_ms/Ctracks/*.ms")

assert len(myvis) == 6

default('concat')
concat(vis=myvis, concatvis='12A-304_lines_Ctracks_all.ms')

default('mstransform')
mstransform(vis='12A-304_lines_Ctracks_all.ms',
            outputvis='12A-304_lines_Ctracks.ms',
            field='M31*',
            datacolumn='corrected',
            spw='',
            mode='channel',
            start=1,
            nchan=-1,
            width=1,
            combinespws=True,
            regridms=True,
            keepflags=False)
