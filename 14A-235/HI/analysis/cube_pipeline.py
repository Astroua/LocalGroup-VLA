
'''
Make signal masks and compute the moments.
'''

from astropy import log
from cube_analysis import run_pipeline


run_042kms = True

num_cores = 4

if run_042kms:
    log.info("Running 0.42 km/s cubes")

    from paths import (fourteenA_HI_data_path,
                       fourteenA_HI_data_wEBHIS_path,)

    # VLA-only cube
    log.info("Masking and moments for the VLA-only cube")
    run_pipeline(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor.fits"),
                 fourteenA_HI_data_path("", no_check=True),
                 pb_file=fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 17,
                                 "min_chan": 5,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": False},
                 combeam_kwargs={})

    # VLA+GBT cube
    log.info("Masking and moments for the VLA+EBHIS cube")
    run_pipeline(fourteenA_HI_data_wEBHIS_path("M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered.fits"),
                 fourteenA_HI_data_wEBHIS_path("", no_check=True),
                 pb_file=fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits"),
                 pb_lim=0.05,
                 apply_pbmasking=False,
                 convolve_to_common_beam=False,
                 masking_kwargs={"method": "ppv_connectivity",
                                 "save_cube": True,
                                 "is_huge": True,
                                 "smooth_chans": 17,
                                 "min_chan": 5,
                                 "peak_snr": 4.,
                                 "min_snr": 2,
                                 "edge_thresh": 1,
                                 "pb_map_name": fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits")
                                 },
                 moment_kwargs={"num_cores": num_cores,
                                "verbose": True,
                                "chunk_size": 1e5,
                                "make_peakvels": False},
                 combeam_kwargs={})
