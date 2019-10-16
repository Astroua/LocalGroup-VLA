
'''
Create feathered VLA cubes with the EBHIS cube.
'''

from spectral_cube import SpectralCube
import os
from os.path import join as osjoin
from astropy import log

from cube_analysis.feather_cubes import feather_cube

from paths import (fifteenA_HI_BC_1_2kms_data_path,
                   fifteenA_HI_BC_1_2kms_data_wEBHIS_path,
                   fifteenA_HI_BCtaper_04kms_data_path,
                   fifteenA_HI_BCtaper_04kms_data_wEBHIS_path,
                   ebhis_m31_HI_data_path,
                   m31_data_path)
from constants import hi_freq

num_cores = 1

run_dict = dict(run_BCDtaper_04kms=False,
                run_BCD_1_2kms=True)

for key in run_dict:

    if not run_dict[key]:
        continue

    # Change filenames and output plots with key name
    if key == 'run_BCDtaper_04kms':

        chunk = 250

        vla_cube = SpectralCube.read(fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.fits"))

        pb_cube = SpectralCube.read(fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits"))

        ebhis_name = ebhis_m31_HI_data_path(
                          "15A-175_items/CAR_C01_15A175_match_04kms_spectralregrid.fits")
        ebhis_cube = SpectralCube.read(ebhis_name)

        save_name = fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.EBHIS_feathered.fits",
                                                  no_check=True)

        output_path = fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("", no_check=True)

    elif key == 'run_BCD_1_2kms':

        chunk = 100

        vla_cube = SpectralCube.read(fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.fits"))

        pb_cube = SpectralCube.read(fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits"))

        ebhis_name = ebhis_m31_HI_data_path(
                          "15A-175_items/CAR_C01_15A175_match_12kms_spectralregrid.fits")
        ebhis_cube = SpectralCube.read(ebhis_name)

        # raise NotImplementedError("")
        save_name = fifteenA_HI_BC_1_2kms_data_wEBHIS_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor.EBHIS_feathered.fits", no_check=True)

        output_path = fifteenA_HI_BC_1_2kms_data_wEBHIS_path("", no_check=True)

    else:
        raise ValueError("")

    # From feather_comparisons.py, we find that EBHIS needs a correction
    # factor of 1.07 applied from comparing with the uv-overlapping region of
    # the VLA data
    # Using the ratio from the full 14A mosaic. No data has been re-weighted
    # and the uv-comparison for this mosaic gives odd results
    ebhis_cube.allow_huge_operations = True
    ebhis_cube *= 1.07

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    feather_cube(vla_cube, ebhis_cube, pb_hi=pb_cube,
                 restfreq=hi_freq, save_feather=True,
                 save_name=save_name, overwrite=True,
                 num_cores=num_cores,
                 # weights=weight,
                 chunk=chunk, verbose=False,
                 relax_spectral_check=False,
                 spec_check_kwargs={'rtol': 0.03})
