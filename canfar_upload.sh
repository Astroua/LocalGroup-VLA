
echo "Run this script on a cirrus instance."

cadc-get-cert --user ekoch

BIGDATA_PATH="/mnt/bigdata/ekoch/"

LGHI_PATH="vos:ekoch/LocalGroup-HI/"

vmkdir $LGHI_PATH

M31HI_PATH="${LGHI_PATH}/M31/"

vmkdir "${M31HI_PATH}"

# Upload the M31 D-config

M31HI_DCONF_PATH="${M31HI_PATH}/M31_HI_Dconfig_58arcsec_0p42kms_wEBHIS/"

fourteenA_DATA_PATH="${BIGDATA_PATH}/M31/VLA/14A-235/HI/full_imaging_wEBHIS/"

vmkdir "${M31HI_DCONF_PATH}"

# Doing this by-hand for now since I have a bunch of other stuff in the local folder.
# Upload archival products

rootname='M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered_K'

vcp --quick "${fourteenA_DATA_PATH}/${rootname}.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.kurtosis.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.lwidth.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.mom0.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.mom1.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.peaktemps.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.peakvels.fits" "${M31HI_DCONF_PATH}"
vcp --quick "${fourteenA_DATA_PATH}/${rootname}.skewness.fits" "${M31HI_DCONF_PATH}"

echo "Finished D config upload"

# Upload the M31 7-pt hex BCD tapered w/ 0.42 km/s channels

M31HI_BCDTAPCONF_PATH="${M31HI_PATH}/M31NorthHex_HI_BCDtaper_18arcsec_0p42kms_wEBHIS/"

fifteenA_TAP_DATA_PATH="${BIGDATA_PATH}/M31/VLA/15A-175/HI/full_imaging_BCD_taper_0_42kms_wEBHIS/"

vmkdir "${M31HI_BCDTAPCONF_PATH}"

rootname='M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.EBHIS_feathered_K'

vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.kurtosis.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.lwidth.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.mom0.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.mom1.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.peaktemps.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.peakvels.fits" "${M31HI_BCDTAPCONF_PATH}"
vcp --quick "${fifteenA_TAP_DATA_PATH}/${rootname}.skewness.fits" "${M31HI_BCDTAPCONF_PATH}"

echo "Finished BCD taper config upload"

# Upload the M31 7-pt hex BCD w/ 1.2 km/s channels

M31HI_BCDCONF_PATH="${M31HI_PATH}/M31NorthHex_HI_BCDtaper_10p5arcsec_1p2kms_wEBHIS/"

fifteenA_DATA_PATH="${BIGDATA_PATH}/M31/VLA/15A-175/HI/full_imaging_1_2kms_wEBHIS/"

vmkdir "${M31HI_BCDCONF_PATH}"

rootname='M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor.EBHIS_feathered_K'

vcp --quick "${fifteenA_DATA_PATH}/${rootname}.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.kurtosis.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.lwidth.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.mom0.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.mom1.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.peaktemps.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.peakvels.fits" "${M31HI_BCDCONF_PATH}"
vcp --quick "${fifteenA_DATA_PATH}/${rootname}.skewness.fits" "${M31HI_BCDCONF_PATH}"

echo "Finished BCD taper config upload"

# M33

M33HI_PATH="${LGHI_PATH}/M33/"

vmkdir "${M33HI_PATH}"

# Upload M33 C config w/ 0.21 km/s

M33HI_CCONF_PATH="${M33HI_PATH}/M33_HI_C_19arcsec_0p21kms_wGBT/"

fourteenB_DATA_PATH="${BIGDATA_PATH}/M33/VLA/14B-088/HI/full_imaging_wGBT/"

vmkdir "${M33HI_CCONF_PATH}"

rootname='M33_14B-088_HI.clean.image.GBT_feathered.pbcov_gt_0.5_masked'

vcp --quick "${fourteenB_DATA_PATH}/${rootname}.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.kurtosis.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.lwidth.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.mom0.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.mom1.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.peaktemps.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.peakvels.fits" "${M33HI_CCONF_PATH}"
vcp --quick "${fourteenB_DATA_PATH}/${rootname}.skewness.fits" "${M33HI_CCONF_PATH}"

echo "Finished M33 C config upload"

# Upload M33 B+C config w/ 1.0 km/s

M33HI_BCCONF_PATH="${M33HI_PATH}/M33_HI_BC_8arcsec_1p0kms_wGBT/"

seventeenB_DATA_PATH="${BIGDATA_PATH}/M33/VLA/17B-162/HI/full_imaging_1kms_wGBT/"

vmkdir "${M33HI_BCCONF_PATH}"

rootname='M33_14B_17B_HI_contsub_width_1kms.image.pbcor.GBT_feathered_K'

vcp --quick "${seventeenB_DATA_PATH}/${rootname}.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.kurtosis.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.lwidth.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.mom0.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.mom1.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.peaktemps.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.peakvels.fits" "${M33HI_BCCONF_PATH}"
vcp --quick "${seventeenB_DATA_PATH}/${rootname}.skewness.fits" "${M33HI_BCCONF_PATH}"

echo "Finished M33 BC config upload"
