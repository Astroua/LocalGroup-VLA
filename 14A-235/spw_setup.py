
#  Line SPW setup for 14A-235 w/ rest frequencies
# SPW $: [Name, Restfreq, Num chans, Chans for uvcontsub]

# Notes for uvcontsub channels:
# UPDARE

# Channel offset b/w cubes made with test_line_imaging.py (excludes edge
# channels) and the full SPW (since we split from the full SPW):
# OH - UPDATE channels
# HI - 205 channels

linespw_dict = {0: ["HI", "1.420405752GHz", 4096, "XXX1240~1560;2820~3410"],
                1: ["OH1612", "1.612231GHz", 512, "XXX53~88;223~240"],  # Currently all flagged
                2: ["OH1665", "1.6654018GHz", 512, "XXX53~88;223~240"],
                3: ["OH1667", "1.667359GHz", 512, "XXX53~88;223~240"],
                4: ["OH1720", "1.72053GHz", 512, "XXX53~88;223~240"],}

fourteenA_sources = {"M31": 'J2000 00h42m44.350 +41d16m08.63',
                     "NGC205": 'J2000 00h40m22.075s +41d41m07.08',
                     "NGC185": 'J2000 00h38m57.970s +48d20m14.56'}
