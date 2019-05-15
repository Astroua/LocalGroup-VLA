
'''
Combine the tracks, then split out the science fields

Treat the B and C config tracks separately
'''

import os
import sys
from glob import glob

from tasks import concat, split

# Which config to combine?

config_num = int(sys.argv[-1])

if config_num not in [0, 1]:
    raise  ValueError("config_num must be 0 or 1. Given {}".format(config_num))

config_settings = {0: ["B", 9], 1: ["C", 11]}

track_folder = "{0}tracks".format(config_settings[config_num][0])

# Grab all of the MS tracks in the folder
myvis = glob("{}/*.speclines.ms".format(track_folder))

assert len(myvis) == config_settings[config_num][1]

concat_name = '15A-175_{}tracks_lines_all.ms'.format(config_settings[config_num][0])

default('concat')
concat(vis=myvis,
       concatvis=concat_name,
       timesort=False)

concat_sci_name = '15A-175_{}tracks_lines.ms'.format(config_settings[config_num][0])

default('split')
split(vis=concat_name, outputvis=concat_sci_name,
      # field='M31*',
      intent='*TARGET*',
      datacolumn='corrected',
      keepflags=False)
