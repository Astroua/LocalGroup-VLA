#  Line SPW setup for 15A-175 w/ rest frequencies
# SPW $: [Name, Restfreq, Num chans, Chans for uvcontsub]

# Notes for uvcontsub channels:
# UPDATE

# Channel offset b/w cubes made with test_line_imaging.py (excludes edge
# channels) and the full SPW (since we split from the full SPW):
# OH - UPDATE channels
# HI - 205 channels

# HI uvcontsub velocity from 108 to 460 km/s and -610 to -1000 km/s
# HI emission from 10 to -320.

linespw_dict = {0: ["HI", "1.420405752GHz", 4096, "205~1075;2805~3750"],
                1: ["OH1612", "1.612231GHz", 512, "XXX66~266"],  # Currently all flagged
                2: ["OH1665", "1.6654018GHz", 512, "XXX66~266"],
                3: ["OH1667", "1.667359GHz", 512, "XXX66~266"],
                4: ["OH1720", "1.72053GHz", 512, "XXX66~266"]}


# XXX UPDATE M31 from -16 to -643 km/s. Native channel width of 0.4122 km/s

# NEEDS TO BE UPDATED
# fifteenA_HI_channels = {"start": 2205, 'end': 3725}
