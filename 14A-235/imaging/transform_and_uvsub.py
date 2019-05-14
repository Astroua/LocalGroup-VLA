
'''
Split out each SPW from the combined MS (concat_and_split.py), convert
to LSRK, and subtract continuum in uv-plane
'''

import os
import sys

from tasks import mstransform, uvcontsub, partition, split

myvis = '14A-235_lines.ms'

spw_num = int(sys.argv[-1])

# Load in the SPW dict in the repo on cedar
execfile(os.path.expanduser("~/code/LocalGroup-VLA/14A-235/spw_setup.py"))
# execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/14A-235/spw_setup.py"))

for source in fourteenA_sources:

    default('mstransform')

    casalog.post("On SPW {}".format(spw_num))

    # Note that the combined MS already only includes the calibrated data
    # with all flagged data removed.

    # If this is HI, we want to keep the continuum version to look for
    # absorption features. Split the uvsubtraction into a separate function

    out_vis = "{0}_14A-235_{1}_spw_{2}_LSRK.ms"\
        .format(source, linespw_dict[spw_num][0], spw_num)

    mstransform(vis=myvis, outputvis=out_vis, spw=str(spw_num),
                datacolumn='data',
                field='{}*'.format(source),
                regridms=True, mode='channel',
                interpolation='linear',  # 'fftshift',
                phasecenter=fourteenA_sources[source],
                restfreq=linespw_dict[spw_num][1], outframe='LSRK',
                douvcontsub=False)

    # Separate uvcontsub call
    uvcontsub(vis=out_vis,
              fitspw='{0}:{1}'.format(spw_num, linespw_dict[spw_num][3]),
              fitorder=0, want_cont=False)
