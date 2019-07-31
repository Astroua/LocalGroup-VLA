
'''
Using really large scales in the multiscale clean makes is susceptible to
diverging. Set the large-scale mask based on the GBT data multiplied by
the pb mask.

Use threshold mask produced by gbt_regrid.py
'''

import os
import numpy as np
from spectral_cube import SpectralCube
from reproject import reproject_interp
from radio_beam import Beam
# from spectral_cube.io.casa_masks import make_casa_mask
import astropy.units as u
from astropy.io import fits
from scipy import ndimage as nd
from astropy.wcs import WCS
from astropy.utils.console import ProgressBar

from cube_analysis.io_utils import create_huge_fits

from paths import (fourteenA_HI_data_path,
                   ebhis_m31_HI_data_path,
                   fifteenA_HI_BC_1_2kms_data_path,
                   fifteenA_HI_BCtaper_04kms_data_path,
                   fourteenA_HI_file_dict,
                   m31_data_path)

run_12kms_BC = True
run_04kms_BC_taper = False

# Define axis in frequency. Then convert to V_rad
freq_0 = 1420434386.2331324 * u.Hz
# This cube averages over 5 channels
del_freq = 1953.2562937736511 * u.Hz

# ~262 for 1.2 km/s
# ~762 for 0.4 km/s


def vel_to_freq(vel_or_freq, rest_freq=1.42040575177 * u.GHz,
                unit=u.Hz):
    '''
    Using radio velocity here.
    '''
    equiv = u.doppler_radio(rest_freq)

    return vel_or_freq.to(unit, equiv)


if run_12kms_BC:

    mask_cube = SpectralCube.read(fourteenA_HI_file_dict["Source_Mask"])

    # Good enough for the mask
    beam = Beam(58 * u.arcsec)
    mask_cube = mask_cube.with_beam(beam)

    vla_pbmask = fits.getdata(fifteenA_HI_BC_1_2kms_data_path("15A_BC_14A_spatial_pbmask.fits")) > 0

    vla_spat_hdr = fits.Header.fromtextfile(fifteenA_HI_BC_1_2kms_data_path("15A_BC_spatial_header.txt"))

    # Hard code in properties to make the spectral axis

    nchan = 262

    # 3 channels
    del_freq *= 3

    freq_axis = np.arange(nchan) * del_freq + freq_0

    vel_axis = vel_to_freq(freq_axis, unit=u.m / u.s)

    save_name = fifteenA_HI_BC_1_2kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BC_spectralregrid_1_2kms.fits",
                                            no_check=True)

    if not os.path.exists(save_name):

        mask_cube = mask_cube.spectral_interpolate(vel_axis)

        if mask_cube._is_huge:
            output_fits = create_huge_fits(save_name, mask_cube.header,
                                           return_hdu=True)

            for chan in ProgressBar(mask_cube.shape[0]):
                output_fits[0].data[chan] = mask_cube[chan].value
            output_fits.flush()
            output_fits.close()
            del output_fits
        else:
            mask_cube.write(save_name, overwrite=True)
    else:
        mask_cube = SpectralCube.read(save_name)
        mask_cube = mask_cube.with_beam(beam)

    # Smooth out the mask and fill in small holes
    beam_element = Beam(1.5 * beam.major).as_tophat_kernel((3 * u.arcsec).to(u.deg)).array > 0

    new_header = mask_cube.header.copy()
    new_header["NAXIS"] = 3
    new_header["NAXIS1"] = vla_pbmask.shape[1]
    new_header["NAXIS2"] = vla_pbmask.shape[0]
    new_header["NAXIS3"] = nchan
    new_header['CRVAL3'] = vel_axis[0].value
    kwarg_skip = ['TELESCOP', 'BUNIT', 'INSTRUME']
    for key in mask_cube.header:
        if key == 'HISTORY' or key == "COMMENT":
            continue
        if key in vla_spat_hdr:
            if "NAXIS" in key:
                continue
            if key in kwarg_skip:
                continue
            new_header[key] = vla_spat_hdr[key]
    new_header.update(mask_cube.beam.to_header_keywords())

    new_header['BITPIX'] = 8
    new_header['BUNIT'] = 'bool'

    save_name = fifteenA_HI_BC_1_2kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BC_1_2kms.fits",
                                            no_check=True)

    output_fits = create_huge_fits(save_name, new_header, return_hdu=True)

    targ_header = WCS(vla_spat_hdr).celestial.to_header()
    targ_header["NAXIS"] = 2
    targ_header["NAXIS1"] = vla_pbmask.shape[1]
    targ_header["NAXIS2"] = vla_pbmask.shape[0]

    for chan in ProgressBar(nchan):
        mask_plane = mask_cube[chan].value.astype(bool)

        mask_plane = nd.binary_dilation(mask_plane, beam_element)

        # Now reproject
        mask_plane = reproject_interp((mask_plane.astype(float), mask_cube[chan].header), targ_header)[0] > 1e-3

        # Apply the pbmask
        mask_plane = np.logical_and(mask_plane, vla_pbmask)

        output_fits[0].data[chan] = mask_plane.astype(">i2")
        if chan % 50 == 0:
            output_fits.flush()

    output_fits.close()

if run_04kms_BC_taper:

    mask_cube = SpectralCube.read(fourteenA_HI_file_dict["Source_Mask"])

    # Good enough for the mask
    beam = Beam(58 * u.arcsec)
    mask_cube = mask_cube.with_beam(beam)

    vla_pbmask = fits.getdata(fifteenA_HI_BCtaper_04kms_data_path("15A_BCtaper_14A_spatial_pbmask.fits")) > 0

    vla_spat_hdr = fits.Header.fromtextfile(fifteenA_HI_BCtaper_04kms_data_path("15A_BCtaper_spatial_header.txt"))

    # Hard code in properties to make the spectral axis

    nchan = 762

    freq_axis = np.arange(nchan) * del_freq + freq_0

    vel_axis = vel_to_freq(freq_axis, unit=u.m / u.s)

    save_name = fifteenA_HI_BCtaper_04kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BCtaper_spectralregrid_0_4kms.fits",
                                            no_check=True)

    if not os.path.exists(save_name):

        mask_cube = mask_cube.spectral_interpolate(vel_axis)

        if mask_cube._is_huge:
            output_fits = create_huge_fits(save_name, mask_cube.header,
                                           return_hdu=True)

            for chan in ProgressBar(mask_cube.shape[0]):
                output_fits[0].data[chan] = mask_cube[chan].value
            output_fits.flush()
            output_fits.close()
            del output_fits
        else:
            mask_cube.write(save_name, overwrite=True)
    else:
        mask_cube = SpectralCube.read(save_name)
        mask_cube = mask_cube.with_beam(beam)

    # Smooth out the mask and fill in small holes
    beam_element = Beam(1.5 * beam.major).as_tophat_kernel((3 * u.arcsec).to(u.deg)).array > 0

    new_header = mask_cube.header.copy()
    new_header["NAXIS"] = 3
    new_header["NAXIS1"] = vla_pbmask.shape[1]
    new_header["NAXIS2"] = vla_pbmask.shape[0]
    new_header["NAXIS3"] = nchan
    new_header['CRVAL3'] = vel_axis[0].value
    kwarg_skip = ['TELESCOP', 'BUNIT', 'INSTRUME']
    for key in mask_cube.header:
        if key == 'HISTORY' or key == "COMMENT":
            continue
        if key in vla_spat_hdr:
            if "NAXIS" in key:
                continue
            if key in kwarg_skip:
                continue
            new_header[key] = vla_spat_hdr[key]
    new_header.update(mask_cube.beam.to_header_keywords())

    new_header['BITPIX'] = 8
    new_header['BUNIT'] = 'bool'

    save_name = fifteenA_HI_BCtaper_04kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BCtaper_0_4kms.fits",
                                            no_check=True)

    output_fits = create_huge_fits(save_name, new_header, return_hdu=True)

    targ_header = WCS(vla_spat_hdr).celestial.to_header()
    targ_header["NAXIS"] = 2
    targ_header["NAXIS1"] = vla_pbmask.shape[1]
    targ_header["NAXIS2"] = vla_pbmask.shape[0]

    for chan in ProgressBar(nchan):
        mask_plane = mask_cube[chan].value.astype(bool)

        mask_plane = nd.binary_dilation(mask_plane, beam_element)

        # Now reproject
        mask_plane = reproject_interp((mask_plane.astype(float), mask_cube[chan].header), targ_header)[0] > 1e-3

        # Apply the pbmask
        mask_plane = np.logical_and(mask_plane, vla_pbmask)

        output_fits[0].data[chan] = mask_plane.astype(">i2")
        if chan % 50 == 0:
            output_fits.flush()

    output_fits.close()
