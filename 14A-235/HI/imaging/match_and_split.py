'''
Match and split the 14A M31 HI data.

'''

import numpy as np
import sys
from glob import glob
import os

from tasks import mstransform, partition, split, concat

# Use astropy's spectral conversion
# Needs to be installed separately
from astropy import units as u

use_contsub = True if sys.argv[-2] == "True" else False

# All in km/s
chan_width = float(sys.argv[-1])
start_vel = -635
end_vel = -6

chan_width_label = "{}kms".format(chan_width).replace(".", "_")
chan_width_quant = chan_width * u.km / u.s

# XXX ~1334 for 0.21 km/s

if use_contsub:
    fourteenA_ms = "M31_14A-235_HI_spw_0_LSRK.ms.contsub"
else:
    fourteenA_ms = "M31_14A-235_HI_spw_0_LSRK.ms"

# Create an MMS prior to splitting to that the split can be run in parallel

fourteenA_mms = "{0}.{1}.regrid".format(fourteenA_ms, chan_width_label)

if os.path.exists(fourteenA_mms):
    casalog.post("Found the regridded 14A MS. Skipping mstransform.")
else:

    casalog.post("Regridding 14A")

    partition(vis=fourteenA_ms,
              outputvis=fourteenA_mms,
              createmms=True,
              flagbackup=False,
              numsubms=31)


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

if not os.path.exists(chan_path):

    os.mkdir(chan_path)

    start = 0

else:

    # Check if some of the channels have already been split
    exist_chans = glob("{}/channel_*".format(chan_path))

    # Didn't find any existing channels
    if len(exist_chans) == 0:
        start = 0

    else:
        # Pick out the channel numbers
        nums = np.array([int(chan.split("_")[-1]) for chan in exist_chans])

        # Assume that the last job stopped while part of the way through
        # the final channel
        final_chan = exist_chans[nums.argmax()]

        os.system("rm -r {}".format(final_chan))

        start = nums.max() - 1

if start == nchan:
    casalog.post("No more channels to split!")
    raise ValueError("No more channels to split!")

for chan in range(start, nchan + 1):

    casalog.post("On splitting channel {}".format(chan))

    ind_chan_path = os.path.join(chan_path,
                                 "channel_{}".format(chan))
    if not os.path.exists(ind_chan_path):
        os.mkdir(ind_chan_path)

    fourA_split_msname = "{0}_channel_{1}.ms".format(fourteenA_ms, chan)
    fourA_split_mmsname = "{0}_channel_{1}.mms".format(fourteenA_ms, chan)

    start_14B = chan * navg_channel + start_14B_chan
    end_14B = (chan + 1) * navg_channel + start_14B_chan - 1

    if navg_channel == 1:
        # These should equal when not averaging channels
        assert start_14B == end_14B
        spw_selec = "0:{0}".format(start_14B)
    else:
        spw_selec = '0:{0}~{1}'.format(start_14B, end_14B)

    mstransform(vis=fourteenA_mms,
                outputvis=os.path.join(ind_chan_path, fourA_split_mmsname),
                datacolumn='data',
                mode='channel',
                field='M31*',
                spw=spw_selec,
                chanaverage=True if navg_channel > 1 else False,
                chanbin=navg_channel)

    # Convert the final MMS to an MS b/c an MMS uses a lot of files and
    # clusters don't like that.
    split(vis=os.path.join(ind_chan_path, fourA_split_mmsname),
          outputvis=os.path.join(ind_chan_path, fourA_split_msname),
          keepmms=False, datacolumn='DATA')

    # Clean-up temporary MS
    os.system("rm -rf {}".format(os.path.join(ind_chan_path, fourA_split_mmsname)))
