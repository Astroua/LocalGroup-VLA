'''
Match and split the 14A M31 HI data.

'''

import numpy as np
import sys
import os

from tasks import mstransform, partition, split

# Use astropy's spectral conversion
# Needs to be installed separately
from astropy import units as u


use_parallel = True

use_contsub = True if sys.argv[-5] == "True" else False

# All in km/s
chan_width = float(sys.argv[-4])
start_vel = -635
end_vel = -6

part = int(sys.argv[-3])
total_parts = int(sys.argv[-2])

out_path = str(sys.argv[-1])

chan_width_label = "{}kms".format(chan_width).replace(".", "_")
chan_width_quant = chan_width * u.km / u.s

# ~1526 for 0.42 km/s

if use_contsub:
    fourteenA_ms = "M31_14A-235_HI_spw_0_LSRK.ms.contsub"
else:
    fourteenA_ms = "M31_14A-235_HI_spw_0_LSRK.ms"


def vel_to_freq(vel_or_freq, rest_freq=1.42040575177 * u.GHz,
                unit=u.Hz):
    '''
    Using radio velocity here.
    '''
    equiv = u.doppler_radio(rest_freq)

    return vel_or_freq.to(unit, equiv)


def closest_channel(freqs, targ_freq):
    return np.argmin(np.abs(freqs - targ_freq))


if use_parallel:
    fourteenA_mms = "{0}.{1}.regrid".format(fourteenA_ms, chan_width_label)

    if os.path.exists(fourteenA_mms):
        casalog.post("Found the 14A MMS. Skipping mstransform.")
    else:
        casalog.post("Regridding 14A")

        partition(vis=fourteenA_ms,
                  outputvis=fourteenA_mms,
                  createmms=True,
                  flagbackup=False,
                  numsubms=31)

else:
    fourteenA_mms = fourteenA_ms


# Get the HI SPW freqs
tb.open(os.path.join(fourteenA_ms, 'SPECTRAL_WINDOW'))
chanfreqs = tb.getcol('CHAN_FREQ').squeeze()
tb.close()

delta_freq = np.abs(np.diff(chanfreqs))[0]

# Find the number of channels to get closest to the requested velocity width
vunit = u.km / u.s
vel_width = \
    np.abs(vel_to_freq(chanfreqs[len(chanfreqs) // 2] * u.Hz, unit=vunit) -
           vel_to_freq(chanfreqs[len(chanfreqs) // 2 - 1] * u.Hz, unit=vunit))

navg_channel = int(round((chan_width_quant / vel_width).value))

start_freq = vel_to_freq(start_vel * u.km / u.s)
end_freq = vel_to_freq(end_vel * u.km / u.s)

# Find the start and finish channels in each MS
start_14A_chan = closest_channel(chanfreqs * u.Hz, start_freq)
end_14A_chan = closest_channel(chanfreqs * u.Hz, end_freq)

if start_14A_chan > end_14A_chan:
    start_14A_chan, end_14A_chan = end_14A_chan, start_14A_chan

nchan_14A = end_14A_chan - start_14A_chan

# Now convert to the number of channels at the expected velocity resolution
nchan = nchan_14A // navg_channel
# Pad number to reach integer factor of navg_channel
if nchan_14A % navg_channel != 0:
    nchan += 1

# Now split out individual channels for imaging.

chan_path = "HI_{0}_{1}".format("contsub" if use_contsub else "nocontsub",
                                chan_width_label)

nchan_part = int(np.ceil(nchan / total_parts))

start = part * nchan_part
end = min((part + 1) * nchan_part, nchan)

for chan in range(start, end):

    casalog.post("On splitting channel {}".format(chan))

    fourA_split_msname = "{0}_channel_{1}.ms".format(fourteenA_ms, chan)
    if use_parallel:
        fourA_split_mmsname = "{0}_channel_{1}.mms".format(fourteenA_ms, chan)
    else:
        fourA_split_mmsname = "{0}_channel_{1}.ms".format(fourteenA_ms, chan)

    # Parallel is to be run on the cedar cluster
    # First check to see if this channel is already saved.
    #
    if use_parallel:
        out_channel = os.path.join(out_path, "channel_{}".format(chan))
        if not os.path.exists(out_channel):
            os.mkdir(out_channel)
        else:
            # Does the MS already exist there? If so, skip it here.
            scratch_ms = os.path.join(out_channel, fourA_split_msname)
            if os.path.exists(scratch_ms):
                casalog.post("Found the split MS for {} in scratch. "
                             "Skipping.".format(chan))

    ind_chan_path = os.path.join(chan_path,
                                 "channel_{}".format(chan))
    if not os.path.exists(ind_chan_path):
        os.mkdir(ind_chan_path)

    start_14A = chan * navg_channel + start_14A_chan
    end_14A = (chan + 1) * navg_channel + start_14A_chan - 1

    if navg_channel == 1:
        # These should equal when not averaging channels
        assert start_14A == end_14A
        spw_selec = "0:{0}".format(start_14A)
    else:
        spw_selec = '0:{0}~{1}'.format(start_14A, end_14A)

    mstransform(vis=fourteenA_mms,
                outputvis=os.path.join(ind_chan_path, fourA_split_mmsname),
                datacolumn='data',
                mode='channel',
                field='M31*',
                spw=spw_selec,
                chanaverage=True if navg_channel > 1 else False,
                chanbin=navg_channel)

    if use_parallel:
        local_split_ms = os.path.join(ind_chan_path, fourA_split_msname)
        local_split_mms = os.path.join(ind_chan_path, fourA_split_mmsname)

        split(vis=local_split_mms,
              outputvis=local_split_ms,
              keepmms=False, datacolumn='DATA')

        os.system("rm -rf {}".format(local_split_mms))

        # Enable copying the new file out to scratch
        out_flag = os.system("cp -r {0} {1}/".format(local_split_ms,
                                                     out_channel))

        # Check that it worked
        if out_flag != 0:
            casalog.post("Copy failed for channel {}".format(chan))
