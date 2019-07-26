
'''
Split out the D-config pointings for a B+C+D image.
'''

import os
import numpy as np

osjoin = os.path.join

fourteenA_path = os.path.expanduser("~/space/ekoch/VLA_tracks/14A-235/products")
fifteenA_path = os.path.expanduser("~/space/ekoch/VLA_tracks/15A-175/products/HI")

# w/ and w/o contsub

myfields = 'M31LARGE_16, M31LARGE_5, M31LARGE_18, M31LARGE_17, M31LARGE_30, M31LARGE_31, M31LARGE_32'

# DATA is calibrated here.
# CORRECTED should be empty.
split(vis=osjoin(fourteenA_path, 'M31_14A-235_HI_spw_0_LSRK.ms'),
      outputvis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms'),
      field=myfields,
      datacolumn='data',
      )

split(vis=osjoin(fourteenA_path, 'M31_14A-235_HI_spw_0_LSRK.ms.contsub'),
      outputvis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms.contsub'),
      field=myfields,
      datacolumn='data',
      )

# There's a 30% offset between frequency channels between 14A and 15A.
# That's a problem for imaging at the 0.4 km/s width.
# transform these to match the 14A frequency.

# Hard code in the # chans and starting point based on the 15A SPW.
# Pad several channels on each side so the averaging at the edges is
# always fine.

fifteenA_C_ms = osjoin(fifteenA_path, "15A-175_Ctracks_HI_spw_0_LSRK.ms")

tb.open(os.path.join(fifteenA_C_ms, 'SPECTRAL_WINDOW'))
chanfreqs_15A_C = tb.getcol('CHAN_FREQ').squeeze()
tb.close()

chan_width = np.diff(chanfreqs_15A_C[:2])[0]

# At orig. channel width
start_15A_C_chan = 1335
nchan_15A_C = 762

start_chan = start_15A_C_chan - 10
nchan = nchan_15A_C + 20


mstransform(vis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms'),
            outputvis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK_freqmatch.ms'),
            datacolumn='data',
            field='M31*',
            spw='0', regridms=True, mode='frequency', veltype='radio',
            start="{}Hz".format(chanfreqs_15A_C[start_chan]),
            width="{}Hz".format(chan_width),
            nchan=nchan,
            interpolation='linear',
            restfreq='1.420405752GHz',
            createmms=False)

mstransform(vis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK.ms.contsub'),
            outputvis=osjoin(fifteenA_path, 'M31_14A-235_15Afields_HI_spw_0_LSRK_freqmatch.ms.contsub'),
            datacolumn='data',
            field='M31*',
            spw='0', regridms=True, mode='frequency', veltype='radio',
            start="{}Hz".format(chanfreqs_15A_C[start_chan]),
            width="{}Hz".format(chan_width),
            nchan=nchan,
            interpolation='linear',
            restfreq='1.420405752GHz',
            createmms=False)
