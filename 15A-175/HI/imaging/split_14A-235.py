
'''
Split out the D-config pointings for a B+C+D image.
'''

import os


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
