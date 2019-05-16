
#  Line SPW setup for 14A-235 w/ rest frequencies
# SPW $: [Name, Restfreq, Num chans, Chans for uvcontsub]

# Notes for uvcontsub channels:
# UPDARE

# Channel offset b/w cubes made with test_line_imaging.py (excludes edge
# channels) and the full SPW (since we split from the full SPW):
# OH - UPDATE channels
# HI - 205 channels

# HI velocity from 66 to 795 km/s
# Use common range for all targets since M31 (at least in the HI) has some
# emission in the dwarf pointings (mostly NGC 205)

linespw_dict = {0: ["HI", "1.420405752GHz", 4096, "235~2005"],
                1: ["OH1612", "1.612231GHz", 512, "66~266"],  # Currently all flagged
                2: ["OH1665", "1.6654018GHz", 512, "66~266"],
                3: ["OH1667", "1.667359GHz", 512, "66~266"],
                4: ["OH1720", "1.72053GHz", 512, "66~266"]}


fourteenA_sources = {"M31": 'J2000 00h42m44.350 +41d16m08.63',
                     "NGC205": 'J2000 00h40m22.075s +41d41m07.08',
                     "NGC185": 'J2000 00h38m57.970s +48d20m14.56'}


# M31 from -16 to -643 km/s. Native channel width of 0.4122 km/s
# NGC 205 from -160 to -370 km/s
# NOTE for NGC 205, get M31 HI emission starting at -243 to -362.
# emission from 205 ends around -260 but including the M31 emission
# to better separate the blue-shifted tail of 205.
# NGC 185 from -157 to -239 km/s

fourteenA_HI_channels = {"M31": {"start": 2205, 'end': 3725},
                         "NGC205": {"start": 2555, 'end': 3065},
                         "NGC185": {"start": 2545, 'end': 2745}}
