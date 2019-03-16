
#  Line SPW setup for 13A-213 w/ rest frequencies
# SPW $: [Name, Restfreq, Num chans, Chans for uvcontsub]


linespw_dict = {0: ["HI", "1.420405752GHz", 2048],
                1: ["H166alp", "1.4247340GHz", 128],
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

galaxy_dict = dict(ic1613={"phasecenter": "J2000 01h04m47.790 +02d07m04.0"},
                   wlm={"phasecenter": "J2000 00h01m58.160 -15d27m39.30"},
                   ngc6822={"phasecenter": "J2000 19h44m57.700 -14d48m12.00"},
                   sextansa={"phasecenter": "J2000 10h11m00.790 -04d41m34.00"})
