
#  Line SPW setup for 13A-213 w/ rest frequencies
# SPW $: [Name, Restfreq, Num chans, Chans for uvcontsub]

# NOTE: Some of the RRL SPWs change! Will need to do a per-target
# spw_dict at some point. HI is always 0, though.
linespw_dict = dict()

linespw_dict['IC1613'] = {0: ["HI", "1.420405752GHz", 2048],
                          1: ["H165alp", "1.45071600", 128],
                          2: ["H164alp", "1.47734GHz", 128],
                          3: ["OH1612", "1.612231GHz", 512],
                          4: ["OH1665", "1.6654018GHz", 512],
                          5: ["OH1667", "1.667359GHz", 512],
                          6: ["H156alp", "1.71567248GHz", 128],
                          7: ["OH1720", "1.72053GHz", 512],
                          8: ["H154alp", "1.78316770GHz", 128],
                          9: ["H153alp", "1.81825GHz", 128],
                          10: ["H152alp", "1.85425GHz", 128],
                          11: ["H151alp", "1.891212GHz", 128]}

linespw_dict['WLM'] = {0: ["HI", "1.420405752GHz", 2048],
                       1: ["H166alp", "1.4247340GHz", 128],
                       2: ["H165alp", "1.45071600", 128],
                       3: ["H164alp", "1.47734GHz", 128],
                       4: ["OH1612", "1.612231GHz", 512],
                       5: ["OH1665", "1.6654018GHz", 512],
                       6: ["OH1667", "1.667359GHz", 512],
                       7: ["H156alp", "1.71567248GHz", 128],
                       8: ["OH1720", "1.72053GHz", 512],
                       9: ["H154alp", "1.78316770GHz", 128],
                       10: ["H153alp", "1.81825GHz", 128],
                       11: ["H152alp", "1.85425GHz", 128]}

linespw_dict['NGC6822'] = {0: ["HI", "1.420405752GHz", 2048],
                           1: ["H165alp", "1.45071600", 128],
                           2: ["H164alp", "1.47734GHz", 128],
                           3: ["OH1612", "1.612231GHz", 512],
                           4: ["OH1665", "1.6654018GHz", 512],
                           5: ["OH1667", "1.667359GHz", 512],
                           6: ["H156alp", "1.71567248GHz", 128],
                           7: ["OH1720", "1.72053GHz", 512],
                           8: ["H154alp", "1.78316770GHz", 128],
                           9: ["H153alp", "1.81825GHz", 128],
                           10: ["H152alp", "1.85425GHz", 128],
                           11: ["H151alp", "1.891212GHz", 128]}

linespw_dict['SextansA'] = {0: ["HI", "1.420405752GHz", 2048],
                            1: ["H165alp", "1.45071600", 128],
                            2: ["H164alp", "1.47734GHz", 128],
                            3: ["OH1612", "1.612231GHz", 512],
                            4: ["OH1665", "1.6654018GHz", 512],
                            5: ["OH1667", "1.667359GHz", 512],
                            6: ["H156alp", "1.71567248GHz", 128],
                            7: ["OH1720", "1.72053GHz", 512],
                            8: ["H155alp", "1.74898600GHz", 128],
                            9: ["H154alp", "1.78316770GHz", 128],
                            10: ["H153alp", "1.81825GHz", 128],
                            11: ["H152alp", "1.85425GHz", 128]}

# Continuum ranges are for HI only
# HI_start and HI_nchan is the start and number of channels to use in the
# final imaging.
galaxy_dict = dict(ic1613={"phasecenter": "J2000 01h04m47.790 +02d07m04.0",
                           "cont_range": "0:750~950;1300~1700",
                           "HI_start": 950,  # Emission at ~1050; ends at ~1220
                           "HI_nchan": 350},
                   wlm={"phasecenter": "J2000 00h01m58.160 -15d27m39.30",
                        "cont_range": "0:200~800;1350~1700",
                        "HI_start": 925,  # Emission at ~1024; ends at ~1257
                        "HI_nchan": 425},
                   ngc6822={"phasecenter": "J2000 19h44m57.700 -14d48m12.00",
                            "cont_range": "0:500~650;1150~1550",
                            "HI_start": 720,
                            "HI_nchan": 700},
                   sextansa={"phasecenter": "J2000 10h11m00.790 -04d41m34.00",
                             "cont_range": "0:150~650;1170~1500",
                             "HI_start": 765,  # Emission at 865; ends at 1075
                             "HI_nchan": 400},)
