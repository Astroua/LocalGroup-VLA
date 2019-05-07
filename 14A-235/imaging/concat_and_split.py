
'''
Combine the tracks, then split out the science fields
'''

import os
import sys
from glob import glob

from tasks import concat, split

# Grab all of the MS tracks in the folder (should be 15)
myvis = glob("*.speclines.ms")

assert len(myvis) == 15

default('concat')
concat(vis=myvis, concatvis='14A-235_lines_all.ms', timesort=False)

default('split')
split(vis='14A-235_lines_all.ms', outputvis='14A-235_lines.ms',
      # field='M31*',
      intent='*TARGET*',
      datacolumn='corrected',
      keepflags=False)

# os.system("rm -r 14A-235_lines_all.ms")
