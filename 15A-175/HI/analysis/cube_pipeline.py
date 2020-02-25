
'''
Make signal masks and compute the moments.
'''

from astropy import log
from cube_analysis import run_pipeline


run_042kms = True
run_1_2kms = True

num_cores = 4

if run_042kms:
    log.info("Running 0.42 km/s cubes")

    from paths import (fifteenA_HI_BCtaper_04kms_data_path,
                       fifteenA_HI_BCtaper_04kms_data_wEBHIS_path)

    mw_hi_mask = fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("M31_15A_taper_interactive_mask.fits")

    # VLA-only cube
    log.info("Masking and moments for the VLA-only cube")
    run_pipeline(fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.fits"),
                 fifteenA_HI_BCtaper_04kms_data_path("", no_check=True),
                 pb_file=fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 convert_to_K=True,
                 skip_existing_mask=True,
                 custom_mask_name=mw_hi_mask,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 17,
                                 "min_chan": 5,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": False},
                 combeam_kwargs={})

    # VLA+GBT cube
    log.info("Masking and moments for the VLA+EBHIS cube")
    run_pipeline(fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.EBHIS_feathered.fits"),
                 fifteenA_HI_BCtaper_04kms_data_wEBHIS_path("", no_check=True),
                 pb_file=fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 convert_to_K=True,
                 skip_existing_mask=True,
                 custom_mask_name=mw_hi_mask,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 17,
                                 "min_chan": 5,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": False},
                 combeam_kwargs={})

if run_1_2kms:
    log.info("Running 1.2 km/s cubes")

    # NOTE: the last few (empty) channels did not complete stage 2 cleaning
    # There's nothing usable in them so we'll exclude them from the moments

    from paths import (fifteenA_HI_BC_1_2kms_data_path,
                       fifteenA_HI_BC_1_2kms_data_wEBHIS_path)

    mw_hi_mask = fifteenA_HI_BC_1_2kms_data_wEBHIS_path("M31_15A_interactive_mask.fits")


    log.info("Masking and moments for the VLA-only cube")
    run_pipeline(fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor.fits"),
                 fifteenA_HI_BC_1_2kms_data_path("", no_check=True),
                 pb_file=fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 convert_to_K=True,
                 skip_existing_mask=True,
                 custom_mask_name=mw_hi_mask,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 6,  # Same as for M33 17B B+C cube
                                 "min_chan": 4,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": True,
                                "smooth_size": 1,
                                "spectral_slice": slice(0, 257)},
                 combeam_kwargs={})

    # VLA+EBHIS cube
    log.info("Masking and moments for the VLA+EBHIS cube")
    run_pipeline(fifteenA_HI_BC_1_2kms_data_wEBHIS_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor.EBHIS_feathered.fits"),
                 fifteenA_HI_BC_1_2kms_data_wEBHIS_path("", no_check=True),
                 pb_file=fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 convert_to_K=True,
                 skip_existing_mask=True,
                 custom_mask_name=mw_hi_mask,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 6,
                                 "min_chan": 4,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": True,
                                "smooth_size": 1,
                                "spectral_slice": slice(0, 257)},
                 combeam_kwargs={})
