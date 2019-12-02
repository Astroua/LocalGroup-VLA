
# Scrap all the brick mosaics for PHAT

import os
from os.path import join as osjoin


output = "/home/ekoch/bigdata/ekoch/M31/PHAT/"

baseurl = "https://archive.stsci.edu/pub/hlsp/phat/"

# This is easier than webscraping right now.
brick_dict = {1: 12058,
              2: 12073,
              3: 12109,
              4: 12107,
              5: 12074,
              6: 12105,
              7: 12113,
              8: 12075,
              9: 12057,
              10: 12111,
              11: 12115,
              12: 12071,
              13: 12114,
              14: 12072,
              15: 12056,
              16: 12106,
              17: 12059,
              18: 12108,
              19: 12110,
              20: 12112,
              21: 12055,
              22: 12076,
              23: 12070}

for i in range(1, 24):

    if i < 10:
        brickurl = f"{baseurl}/brick0{i}"

        acs_475 = f"hlsp_phat_hst_acs-wfc_{brick_dict[i]}-m31-b0{i}_f475w_v1_drz.fits"
        acs_814 = f"hlsp_phat_hst_acs-wfc_{brick_dict[i]}-m31-b0{i}_f814w_v1_drz.fits"
        wfcir_110 = f"hlsp_phat_hst_wfc3-ir_{brick_dict[i]}-m31-b0{i}_f110w_v1_drz.fits"
        wfcir_160 = f"hlsp_phat_hst_wfc3-ir_{brick_dict[i]}-m31-b0{i}_f160w_v1_drz.fits"
        wfcuv_275 = f"hlsp_phat_hst_wfc3-uvis_{brick_dict[i]}-m31-b0{i}_f275w_v1_drz.fits"
        wfcuv_336 = f"hlsp_phat_hst_wfc3-uvis_{brick_dict[i]}-m31-b0{i}_f336w_v1_drz.fits"
    else:
        brickurl = f"{baseurl}/brick{i}"

        acs_475 = f"hlsp_phat_hst_acs-wfc_{brick_dict[i]}-m31-b{i}_f475w_v1_drz.fits"
        acs_814 = f"hlsp_phat_hst_acs-wfc_{brick_dict[i]}-m31-b{i}_f814w_v1_drz.fits"
        wfcir_110 = f"hlsp_phat_hst_wfc3-ir_{brick_dict[i]}-m31-b{i}_f110w_v1_drz.fits"
        wfcir_160 = f"hlsp_phat_hst_wfc3-ir_{brick_dict[i]}-m31-b{i}_f160w_v1_drz.fits"
        wfcuv_275 = f"hlsp_phat_hst_wfc3-uvis_{brick_dict[i]}-m31-b{i}_f275w_v1_drz.fits"
        wfcuv_336 = f"hlsp_phat_hst_wfc3-uvis_{brick_dict[i]}-m31-b{i}_f336w_v1_drz.fits"

    print(f"Downloading brick {i}")

    brick_path = osjoin(output, f"brick{i}")
    if not os.path.exists(brick_path):
        os.mkdir(brick_path)

    os.chdir(brick_path)

    for file in [acs_475, acs_814, wfcir_110, wfcir_160, wfcuv_275, wfcuv_336]:

        # Check if we need to download again
        if os.path.exists(file):
            continue

        os.system(f"wget {osjoin(brickurl, file)}")

    # os.system(f"wget {osjoin(brickurl, acs_814)}")
    # os.system(f"wget {osjoin(brickurl, wfcir_110)}")
    # os.system(f"wget {osjoin(brickurl, wfcir_160)}")
    # os.system(f"wget {osjoin(brickurl, wfcuv_275)}")
    # os.system(f"wget {osjoin(brickurl, wfcuv_336)}")
