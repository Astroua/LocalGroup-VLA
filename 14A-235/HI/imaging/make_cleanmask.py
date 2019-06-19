
'''
Using really large scales in the multiscale clean makes is susceptible to
diverging. Set the large-scale mask based on the GBT data multiplied by
the pb mask.

Use threshold mask produced by gbt_regrid.py
'''

from astropy.io import fits
from astropy.wcs import WCS
from spectral_cube import SpectralCube
from astropy.utils.console import ProgressBar
import numpy as np
import os
import astropy.units as u

from cube_analysis.io_utils import create_huge_fits

from paths import (fourteenA_HI_data_path,
                   ebhis_m31_HI_data_path)

osjoin = os.path.join

run_04kms = True
# run_1kms = True


if run_04kms:

    ebhis_outpath = ebhis_m31_HI_data_path('14A-235_items', no_check=True)

    cube_name = "CAR_C01_14A235_match_04kms.fits"

    save_name = osjoin(ebhis_outpath, cube_name)

    ebhis_cube = SpectralCube.read(save_name)

    t_cut = 1 * u.K

    vla_pbmask = fits.getdata(fourteenA_HI_data_path("14A_spatial_pbmask.fits")) > 0

    vla_spat_hdr = fits.Header.fromtextfile(fourteenA_HI_data_path("14A_spatial_header.txt"))

    new_header = ebhis_cube.header.copy()
    new_header['BITPIX'] = 8
    new_header['BUNIT'] = 'bool'

    out_name = "CAR_C01_14A235_match_04kms_1K_mask.fits"
    save_name = osjoin(ebhis_outpath, out_name)
    output_fits = create_huge_fits(save_name, new_header, return_hdu=True)

    for chan in ProgressBar(ebhis_cube.shape[0]):
        mask_chan = ebhis_cube[chan] > t_cut
        # Set cut-off at pb mask
        mask_chan = np.logical_and(mask_chan, vla_pbmask)
        output_fits[0].data[chan] = mask_chan
        if chan % 100 == 0:
            output_fits.flush()
    output_fits.close()

    del output_fits
