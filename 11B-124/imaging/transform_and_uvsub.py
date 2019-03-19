
'''
Split out each SPW from the combined MS (concat_and_split.py), convert
to LSRK, and subtract continuum in uv-plane
'''

import os

from tasks import mstransform, uvcontsub, partition, split

myvis = '11B-124_lines.ms'


default('mstransform')

# Note that the combined MS already only includes the calibrated data
# with all flagged data removed.

# If this is HI, we want to keep the continuum version to look for
# absorption features. Split the uvsubtraction into a separate function

spw_num = 0
line_name = "HI"

casalog.post("On SPW {}".format(spw_num))

do_uvcontsub = False
out_vis = "11B-124_{0}_spw_{1}_LSRK.ms"\
    .format(line_name, spw_num)

mstransform(vis=myvis, outputvis=out_vis, spw=str(spw_num),
            datacolumn='data',
            regridms=True, mode='channel', interpolation='fftshift',
            phasecenter='J2000 01h33m50.904 +30d39m35.79',
            restfreq="1.420405752GHz", outframe='LSRK',
            douvcontsub=do_uvcontsub)

# Separate uvcontsub for HI
out_vis_cs = "11B-124_{0}_spw_{1}_LSRK.ms.contsub"\
    .format(line_name, spw_num)

out_mms_vis_cs = "11B-124_{0}_spw_{1}_LSRK.mms.contsub"\
     .format(line_name, spw_num)

# The operation is much fast in parallel, so make an MMS and then
# convert back
partition(vis=out_vis, outputvis=out_vis[:-3] + ".mms", createmms=True,
          separationaxis='auto', flagbackup=False)

uvcontsub(vis=out_vis[:-3] + ".mms",
          fitspw='0:30~100;876~1070',
          fitorder=0, want_cont=False)

default('split')
split(vis=out_mms_vis_cs, outputvis=out_vis_cs, keepmms=False)
