# Local runs on SegFault

num_core=6

# IC1613
cd /mnt/space/ekoch/VLA_tracks/13A-213/IC1613/products/HI/
# 0.4 km/s contsub
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py True 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py True 1 natural 2
# 0.4 km/s no contsub
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py False 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py False 1 natural 2

# robust weighting
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py True 1 briggs 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/IC1613_C_config_imaging.py True 1 briggs 2

# WLM
# 0.4 km/s contsub
cd /mnt/space/ekoch/VLA_tracks/13A-213/WLM/products/HI/
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py True 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py True 1 natural 2
# 0.4 km/s no contsub
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py False 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py False 1 natural 2

# robust weighting
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py True 1 briggs 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/WLM_DnC_config_imaging.py True 1 briggs 2

# Sextans A
# All tracks, C+D
# 0.4 km/s contsub
cd /mnt/space/ekoch/VLA_tracks/13A-213/SextansA/products/HI/
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_D_config_imaging.py True 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_D_config_imaging.py True 1 natural 2

# 0.4 km/s contsub tapered to a D config beam (max sensitivity)
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_D_config_taper_imaging.py True 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_D_config_taper_imaging.py True 1 natural 2

# C-only tracks
# 0.4 km/s contsub
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py True 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py True 1 natural 2
# 0.4 km/s no contsub
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py False 1 natural 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py False 1 natural 2

# robust weighting
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py True 1 briggs 1
~/casa-release-5.5.0-149.el7/bin/mpicasa -n $num_core ~/casa-release-5.5.0-149.el7/bin/casa -c ~/ownCloud/code_development/LocalGroup-VLA/13A-213/HI/imaging/SextansA_C_config_imaging.py True 1 briggs 2

