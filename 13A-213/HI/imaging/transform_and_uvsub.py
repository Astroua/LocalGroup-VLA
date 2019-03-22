
'''
Convert HI spw (0) to LSRK, and subtract continuum in uv-plane.
'''

import os
import sys

from tasks import mstransform, uvcontsub

# galaxy name given. And is folder name
gal_name = sys.argv[-1]

myvis = '13A-213_{}_spw0.ms'.format(gal_name)

# Load in the info dicts from the repo
execfile(os.path.expanduser("~/code/LocalGroup-VLA/13A-213/spw_setup.py"))

default('mstransform')

spw_num = 0
line_name = "HI"

casalog.post("On SPW {}".format(spw_num))

out_vis = "{}_LSRK.ms".format(myvis.rstrip(".ms"))

mstransform(vis=myvis, outputvis=out_vis, spw=str(spw_num),
            datacolumn='data',
            regridms=True, mode='channel', interpolation='fftshift',
            phasecenter=galaxy_dict[gal_name.lower()]['phasecenter'],
            restfreq="1.420405752GHz", outframe='LSRK',
            douvcontsub=False)

# Separate uvcontsub for HI
out_vis_cs = "{}_LSRK.ms.contsub".format(myvis.rstrip(".ms"))


uvcontsub(vis=out_vis,
          fitspw=galaxy_dict[gal_name.lower()]['cont_range'],
          fitorder=0, want_cont=False, datacolumn='data')
