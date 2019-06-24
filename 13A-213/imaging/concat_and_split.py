
'''
Combine the tracks, then split out the science fields
'''

import os
import sys
from glob import glob

from tasks import concat, split


data_path = os.path.expanduser("~/space/ekoch/VLA_tracks/13A-213/")

# CHANGE TO RUN INDIVIDUAL GALAXIES
gal = str(sys.argv[-1])

os.chdir(os.path.join(data_path, gal))

# Grab all of the MS tracks in the folder (should be 17)
myvis = glob("calibrated/*.speclines.ms")

# Expected number of tracks for each galacy
track_names = {'WLM': 2, "NGC6822": 1, "SextansA": 6, "IC1613": 3}

assert len(myvis) == track_names[gal]

default('concat')
concat(vis=myvis, concatvis='products/{}_13A-213_lines_all.ms'.format(gal),
       timesort=False)

if gal == 'WLM':
    field_name = 'Wolf*'
else:
    field_name = '{}*'.format(gal)

default('split')
split(vis='products/{}_13A-213_lines_all.ms'.format(gal),
      outputvis='products/{}_13A-213_lines.ms'.format(gal),
      field=field_name,
      datacolumn='corrected',
      keepflags=False)

# default('split')
# split(vis='17B-162_lines_all.ms',
#       outputvis='17B-162_lines_cals.ms',
#       field='J0319+4130,*3C138,*3C48',
#       datacolumn='corrected',
#       keepflags=False)

# os.system("rm -r 17B-162_lines_all.ms")
