
'''
Combine the tracks, then split out the science fields
'''

import os
import sys
from glob import glob

from tasks import concat, mstransform

# Grab all of the MS tracks in the folder (should be 10)
myvis = glob("orig_ms/*.ms")

assert len(myvis) == 10

default('concat')
concat(vis=myvis, concatvis='11B-124_lines_all.ms')

default('mstransform')
mstransform(vis='11B-124_lines_all.ms',
            outputvis='11B-124_lines.ms',
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

# os.system("rm -r 11B-124_lines_all.ms")
