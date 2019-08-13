'''
Match and split the re-weighted HI MSs
The 14B frequency range includes 2000 channels. That same range in the 17B
data is 2006 channels. So we first regrid and split the data over the same
velocity range. The original channels are -206 and
change m/s. Regrid to something common like -210 m/s.

UPDATE: The issue with this regridding is that there is a beat pattern
when changing the channel widths by the such a small amount. CASA 5.3
*seemed* to actually be using linear interpolation, not the FFT shift.
When using the FFT shift in CASA 5.4 on other data, it caused horrific
residuals in the spectral dimension. Unsure why. However, the two
data sets have the same frequency channel width (0.977 kHz) and have a
frequency offset of 0.2% of the channel width. I'm just going to
match frequency bins to the nearest velocity instead of regridding.
For larger channel sizes, I'll round down to the nearest integer.

The individual channels are then split out for imaging. A separate
folder structure is made for each choice of channel width.

The input given is the channel width in km/s. It is assumed that
the start and end points will be the same (or rounded up by 1),
'''

import numpy as np
import sys
from glob import glob
import os

from tasks import mstransform, partition, split, concat

# Use astropy's spectral conversion
# Needs to be installed separately
from astropy import units as u

# This is here for local runs to avoid needing to make an MMS
# Mostly for storage reasons.
use_parallel = False

use_contsub = True if sys.argv[-5] == "True" else False

# All in km/s
chan_width = float(sys.argv[-4])
# Capture about half of M31's velocity range in these
start_vel = -320
end_vel = -6

part = int(sys.argv[-3])
total_parts = int(sys.argv[-2])

out_path = str(sys.argv[-1])

chan_width_label = "{}kms".format(chan_width).replace(".", "_")
chan_width_quant = chan_width * u.km / u.s

# Common fields in B and C
myfields = 'M31*'

# ~262 for 1.2 km/s
# ~762 for 0.4 km/s
# n_chan = int(np.ceil((end_vel - start_vel) / chan_width))

fourteenA_ms = "M31_14A-235_15Afields_HI_spw_0_LSRK_freqmatch.ms"
fifteenA_B_ms = "15A-175_Btracks_HI_spw_0_LSRK.ms"
fifteenA_C_ms = "15A-175_Ctracks_HI_spw_0_LSRK.ms"

fourteenA_mms = "{0}.{1}.regrid".format(fourteenA_ms, chan_width_label)
fifteenA_B_mms = "{0}.{1}.regrid".format(fifteenA_B_ms, chan_width_label)
fifteenA_C_mms = "{0}.{1}.regrid".format(fifteenA_C_ms, chan_width_label)

concat_vis = '14A_15A_HI_LSRK.ms'

if use_contsub:

    fourteenA_ms += ".contsub"
    fifteenA_B_ms += ".contsub"
    fifteenA_C_ms += ".contsub"
    concat_vis += ".contsub"

# Create an MMS prior to splitting to that the split can be run in parallel

all_ms = [fourteenA_ms, fifteenA_B_ms, fifteenA_C_ms]


if use_parallel:

    all_mms = [fourteenA_mms, fifteenA_B_mms, fifteenA_C_mms]

    for myms, mymms in zip(all_ms, all_mms):

        if os.path.exists(mymms):
            casalog.post("Found {}. Skipping mstransform.".format(mymms))
            continue

        partition(vis=myms,
                  outputvis=mymms,
                  createmms=True,
                  flagbackup=False,
                  numsubms=31)  # Assuming this is run on a 32-core node.

else:
    all_mms = all_ms


def vel_to_freq(vel_or_freq, rest_freq=1.42040575177 * u.GHz,
                unit=u.Hz):
    '''
    Using radio velocity here.
    '''
    equiv = u.doppler_radio(rest_freq)

    return vel_or_freq.to(unit, equiv)


def closest_channel(freqs, targ_freq):
    return np.argmin(np.abs(freqs - targ_freq))


# Get the HI SPW freqs
tb.open(os.path.join(fourteenA_ms, 'SPECTRAL_WINDOW'))
chanfreqs_14A = tb.getcol('CHAN_FREQ').squeeze()
tb.close()

delta_freq_14A = np.abs(np.diff(chanfreqs_14A))[0]


tb.open(os.path.join(fifteenA_B_ms, 'SPECTRAL_WINDOW'))
chanfreqs_15A_B = tb.getcol('CHAN_FREQ').squeeze()
tb.close()

delta_freq_15A_B = np.abs(np.diff(chanfreqs_15A_B))[0]

tb.open(os.path.join(fifteenA_C_ms, 'SPECTRAL_WINDOW'))
chanfreqs_15A_C = tb.getcol('CHAN_FREQ').squeeze()
tb.close()

delta_freq_15A_C = np.abs(np.diff(chanfreqs_15A_C))[0]

# They should be really close
# Within 0.33 kHz, 10^-5 of the channel width.
assert abs(delta_freq_15A_B - delta_freq_15A_C) < 0.5
assert abs(delta_freq_14A - delta_freq_15A_C) < 0.5

# Find the number of channels to get closest to the requested velocity width
vunit = u.km / u.s
vel_width = \
    np.abs(vel_to_freq(chanfreqs_14A[len(chanfreqs_14A) // 2] * u.Hz, unit=vunit) -
           vel_to_freq(chanfreqs_14A[len(chanfreqs_14A) // 2 - 1] * u.Hz, unit=vunit))

navg_channel = int(round((chan_width_quant / vel_width).value))

start_freq = vel_to_freq(start_vel * u.km / u.s)
end_freq = vel_to_freq(end_vel * u.km / u.s)

# Find the start and finish channels in each MS
start_14A_chan = closest_channel(chanfreqs_14A * u.Hz, start_freq)
end_14A_chan = closest_channel(chanfreqs_14A * u.Hz, end_freq)

if start_14A_chan > end_14A_chan:
    start_14A_chan, end_14A_chan = end_14A_chan, start_14A_chan

start_15A_B_chan = closest_channel(chanfreqs_15A_B * u.Hz, start_freq)
end_15A_B_chan = closest_channel(chanfreqs_15A_B * u.Hz, end_freq)

if start_15A_B_chan > end_15A_B_chan:
    start_15A_B_chan, end_15A_B_chan = end_15A_B_chan, start_15A_B_chan

# NOTE: Due to rounding <<chan_width, we need to +1 to end_15A_B_chan
# Then the max offset between channels always remains much smaller than the
# original channel width
end_15A_B_chan += 1

start_15A_C_chan = closest_channel(chanfreqs_15A_C * u.Hz, start_freq)
end_15A_C_chan = closest_channel(chanfreqs_15A_C * u.Hz, end_freq)

if start_15A_C_chan > end_15A_C_chan:
    start_15A_C_chan, end_15A_C_chan = end_15A_C_chan, start_15A_C_chan


# Channel number in terms of original channel widths
nchan_14A = end_14A_chan - start_14A_chan
nchan_15A_B = end_15A_B_chan - start_15A_B_chan
nchan_15A_C = end_15A_C_chan - start_15A_C_chan

# These need to be the same. Catch possible rounding errors
assert nchan_14A == nchan_15A_C
assert nchan_14A == nchan_15A_B

# Now convert to the number of channels at the expected velocity resolution
nchan = nchan_14A // navg_channel
# Pad number to reach integer factor of navg_channel
if nchan_14A % navg_channel != 0:
    nchan += 1

# Now split out individual channels for imaging.

chan_path = "HI_{0}_{1}".format("contsub" if use_contsub else "nocontsub",
                                chan_width_label)

if not os.path.exists(chan_path):
    os.mkdir(chan_path)

nchan_part = int(np.ceil(nchan / total_parts))

start = part * nchan_part
end = min((part + 1) * nchan_part, nchan)

start_chans = [start_14A_chan, start_15A_B_chan, start_15A_C_chan]

for chan in range(start, end):

    casalog.post("On splitting channel {}".format(chan))

    # Parallel is to be run on the cedar cluster
    # First check to see if this channel is already saved.
    #

    ind_chan_path = os.path.join(chan_path,
                                 "channel_{}".format(chan))
    if not os.path.exists(ind_chan_path):
        os.mkdir(ind_chan_path)

    concat_vis_name = '{0}_chan_{1}'.format(concat_vis, chan)
    concat_ms = os.path.join(ind_chan_path,
                             concat_vis_name)

    if use_parallel:
        out_channel = os.path.join(out_path, "channel_{}".format(chan))
        if not os.path.exists(out_channel):
            os.mkdir(out_channel)
        else:
            # Does the MS already exist there? If so, skip it here.
            scratch_ms = os.path.join(out_channel, concat_vis_name)
            if os.path.exists(scratch_ms):
                casalog.post("Found the split + concat MS for {} in scratch. "
                             "Skipping.".format(chan))

    chan_mss = []

    # Loop through splitting for the 3 MSs
    for my_mms, my_ms, start_chan_obs in zip(all_mms, all_ms, start_chans):

        chan_msname = "{0}_channel_{1}.ms".format(my_ms, chan)
        if use_parallel:
            chan_mmsname = "{0}_channel_{1}.mms".format(my_mms, chan)
        else:
            chan_mmsname = chan_msname

        starter = chan * navg_channel + start_chan_obs
        ender = (chan + 1) * navg_channel + start_chan_obs - 1

        if navg_channel == 1:
            # These should equal when not averaging channels
            assert starter == ender
            spw_selec = "0:{0}".format(starter)
        else:
            spw_selec = '0:{0}~{1}'.format(starter, ender)

        mstransform(vis=my_mms,
                    outputvis=os.path.join(ind_chan_path, chan_mmsname),
                    datacolumn='data',
                    mode='channel',
                    field=myfields,
                    spw=spw_selec,
                    chanaverage=True if navg_channel > 1 else False,
                    chanbin=navg_channel)

        local_split_ms = os.path.join(ind_chan_path, chan_msname)
        local_split_mms = os.path.join(ind_chan_path, chan_mmsname)

        if use_parallel:

            # Convert the final MMS to an MS b/c an MMS uses a lot of files and
            # clusters don't like that.
            split(vis=local_split_mms,
                  outputvis=local_split_ms,
                  keepmms=False, datacolumn='DATA')

            # Remove the split MMS
            os.system("rm -rf {}".format(local_split_mms))

        chan_mss.append(local_split_ms)


    # If the concat ms already exists, delete it. Otherwise more data
    # will be appended on
    if os.path.exists(concat_ms):
        os.system("rm -rf {}".format(concat_ms))

    concat(vis=chan_mss,
           concatvis=concat_ms)

    # Remove the non-concatenated MSs

    for chan_ms in chan_mss:
        os.system("rm -rf {}".format(chan_ms))
