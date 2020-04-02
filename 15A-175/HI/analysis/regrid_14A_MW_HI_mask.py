
'''
Create a MW HI mask from the 14A version. The latter has
higher sensitivity and should be directly applicable for
the higher-res 15A cubes.
'''


import os
from os.path import join as osjoin

from cube_analysis.reprojection import reproject_cube

from paths import (fifteenA_HI_BCtaper_04kms_data_wEBHIS_path,
                   fourteenA_HI_data_wEBHIS_path)


custom_mask_name=fourteenA_HI_data_wEBHIS_path("M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered_interactive_mask.fits")

targ_cube = fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.EBHIS_feathered.fits")

out_path = fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("",
                                                      no_check=True)

reproject_cube(custom_mask_name,
               targ_cube,
               "M31_15A_taper_interactive_mask.fits",
               output_folder=out_path,
               save_spectral=False,
               is_huge=True,
               reproject_type='all',
               common_beam=False,
               verbose=True,
               chunk=80)

# And regrid for the high-res cube.


