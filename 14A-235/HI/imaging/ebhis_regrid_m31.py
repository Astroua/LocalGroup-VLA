
'''
Regrid the EBHIS data to match the 14A footprint.
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
                   ebhis_m31_HI_data_path,
                   m31_data_path)
from constants import hi_freq

osjoin = os.path.join

def vel_to_freq(vel_or_freq, rest_freq=1.42040575177 * u.GHz,
                unit=u.Hz):
    '''
    Using radio velocity here.
    '''
    equiv = u.doppler_radio(rest_freq)

    return vel_or_freq.to(unit, equiv)


run_04kms = True

ebhis_outpath = ebhis_m31_HI_data_path('14A-235_items', no_check=True)

if not os.path.exists(ebhis_outpath):
    os.mkdir(ebhis_outpath)

ebhis_name = "CAR_C01.fits"

cube = SpectralCube.read(ebhis_m31_HI_data_path(ebhis_name))

if run_04kms:

    out_name = "CAR_C01_14A235_match_04kms.fits"
    out_name_specregrid = "CAR_C01_14A235_match_04kms_spectralregrid.fits"

    # We require the spatial pb mask and a saved FITS header that defines the spatial
    # WCS information of the VLA cube
    vla_pbmask = fits.getdata(fourteenA_HI_data_path("14A_spatial_pbmask.fits")) > 0

    vla_spat_hdr = fits.Header.fromtextfile(fourteenA_HI_data_path("14A_spatial_header.txt"))

    # Hard code in properties to make the spectral axis

    # Define axis in frequency. Then convert to V_rad
    freq_0 = 1420433643.3212132 * u.Hz
    # This cube averages over 5 channels
    del_freq = 1952.9365057945251 * u.Hz
    nchan = 1526

    freq_axis = np.arange(nchan) * del_freq + freq_0

    vel_axis = vel_to_freq(freq_axis, unit=u.m / u.s)

    save_name = osjoin(ebhis_outpath, out_name_specregrid)

    # Spectral interpolation, followed by reprojection.
    if not os.path.exists(save_name):

        cube = cube.spectral_interpolate(vel_axis)

        if cube._is_huge:
            output_fits = create_huge_fits(save_name, cube.header,
                                           return_hdu=True)

            for chan in ProgressBar(cube.shape[0]):
                output_fits[0].data[chan] = cube[chan].value
            output_fits.flush()
            output_fits.close()
        else:
            cube.write(save_name, overwrite=True)
    else:
        cube = SpectralCube.read(save_name)

    # Make the reprojected header
    new_header = cube.header.copy()
    new_header["NAXIS"] = 3
    new_header["NAXIS1"] = vla_pbmask.shape[1]
    new_header["NAXIS2"] = vla_pbmask.shape[0]
    new_header["NAXIS3"] = nchan
    new_header['CRVAL3'] = vel_axis[0].value
    # COMMENT is in here b/c casa adds an illegal comment format
    kwarg_skip = ['TELESCOP', 'BUNIT', 'INSTRUME', 'COMMENT']
    for key in cube.header:
        if key == 'HISTORY':
            continue
        if key in vla_spat_hdr:
            if "NAXIS" in key:
                continue
            if key in kwarg_skip:
                continue
            new_header[key] = vla_spat_hdr[key]
    new_header.update(cube.beam.to_header_keywords())
    new_header["BITPIX"] = -32

    # Build up the reprojected cube per channel
    save_name = osjoin(ebhis_outpath, out_name)
    output_fits = create_huge_fits(save_name, new_header, return_hdu=True)

    targ_header = WCS(vla_spat_hdr).celestial.to_header()
    targ_header["NAXIS"] = 2
    targ_header["NAXIS1"] = vla_pbmask.shape[1]
    targ_header["NAXIS2"] = vla_pbmask.shape[0]

    for chan in ProgressBar(cube.shape[0]):
        reproj_chan = \
            cube[chan].reproject(targ_header).value.astype(np.float32)
        output_fits[0].data[chan] = reproj_chan
        if chan % 100 == 0:
            output_fits.flush()
    output_fits.close()

    del output_fits

del cube
