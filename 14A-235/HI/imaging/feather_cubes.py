
'''
Create feathered VLA cubes with the EBHIS cube.
'''

from spectral_cube import SpectralCube
import os
from os.path import join as osjoin
from astropy import log

from cube_analysis.feather_cubes import feather_cube

from paths import (fourteenA_HI_data_path,
                   fourteenA_HI_data_wEBHIS_path,
                   ebhis_m31_HI_data_path,
                   m31_data_path)
from constants import hi_freq

# Set which of the cubes to feather
run_ebhis_0_42kms = True

num_cores = 1
chunk = 300


if run_ebhis_0_42kms:
    log.info("Feathering with 0.42 km/s EBHIS")

    # Load the non-pb masked cube
    vla_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.image.fits"))

    pb_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits"))

    ebhis_name = ebhis_m31_HI_data_path(
                      "14A-235_items/CAR_C01_14A235_match_04kms_spectralregrid.fits")
    ebhis_cube = SpectralCube.read(ebhis_name)

    # From feather_comparisons.py, we find that EBHIS needs a correction factor of 1.07
    # applied from comparing with the uv-overlapping region of the VLA data
    ebhis_cube.allow_huge_operations = True
    ebhis_cube *= 1.07

    output_path = fourteenA_HI_data_wEBHIS_path("", no_check=True)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    save_name = fourteenA_HI_data_wEBHIS_path("M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered.fits",
                                              no_check=True)

    feather_cube(vla_cube, ebhis_cube, pb_hi=pb_cube,
                 restfreq=hi_freq, save_feather=True,
                 save_name=save_name, overwrite=True,
                 num_cores=num_cores,
                 # weights=weight,
                 chunk=chunk, verbose=False,
                 relax_spectral_check=False,
                 spec_check_kwargs={'rtol': 0.03})

    # Now resave a minimal version of the feathered cube
    # The cubes is only ~14 GB. Should be fine on SegFault.
    # Nope. Causes big crash. Avoid.
    # cube = SpectralCube.read(save_name)
    # cube.minimal_subcube().write(save_name, overwrite=True)
    # del cube
