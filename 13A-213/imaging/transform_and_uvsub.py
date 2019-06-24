
'''
Split out each SPW from the combined MS (concat_and_split.py), convert
to LSRK, and subtract continuum in uv-plane
'''

import os
import sys
import socket

from tasks import mstransform, uvcontsub

data_path = os.path.expanduser("~/space/ekoch/VLA_tracks/13A-213/")

# CHANGE TO RUN INDIVIDUAL GALAXIES
gal = str(sys.argv[-1])

os.chdir(os.path.join(data_path, gal, 'products'))

myvis = '{}_13A-213_lines.ms'.format(gal)


# Load in the SPW dict in the repo on cedar
if socket.gethostname().lower() == 'segfault':
    execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/13A-213/spw_setup.py"))
else:
    execfile(os.path.expanduser("~/code/LocalGroup-VLA/13A-213/spw_setup.py"))

# Loop through lines
for spw_num in linespw_dict[gal]:

    line_name = linespw_dict[gal][spw_num][0]
    rest_freq = linespw_dict[gal][spw_num][1]
    num_chan = linespw_dict[gal][spw_num][2]

    default('mstransform')

    casalog.post("On SPW {}".format(spw_num))

    # Note that the combined MS already only includes the calibrated data
    # with all flagged data removed.

    out_vis = "{0}_13A-213_{1}_spw_{2}_LSRK.ms"\
        .format(gal, line_name, spw_num)


    # in casa 5.4.1, fftshift does something that is not linear interpolation
    # but it gives severe edge effects when I've used it on the 13A-213 data
    if gal == 'WLM':
        field_name = 'Wolf*'
    else:
        field_name = '{}*'.format(gal)

    mstransform(vis=myvis, outputvis=out_vis, spw=str(spw_num),
                datacolumn='data',
                field=field_name,
                regridms=True, mode='channel',
                interpolation='linear',  # 'fftshift',
                phasecenter=galaxy_dict[gal.lower()]['phasecenter'],
                restfreq=rest_freq, outframe='LSRK',
                douvcontsub=False)

    default('uvcontsub')

    if spw_num == 0:
        # HI continuum ranges from spw_setup
        fitspw = galaxy_dict[gal.lower()]['cont_range']
    else:
        # RRLs and OH will basically be empty.
        # Use the 25~40 and 60~75 percentiles of the SPW
        bottom = (num_chan * np.array([0.25, 0.40])).astype(int)
        top = (num_chan * np.array([0.60, 0.75])).astype(int)

        fitspw = "0:{0}~{1};{2}~{3}".format(bottom[0], bottom[1],
                                            top[0], top[1])
    # Separate uvcontsub call
    uvcontsub(vis=out_vis,
              fitspw=fitspw,
              fitorder=0, want_cont=False)
