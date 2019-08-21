# Not a cluster submission script! Run on SegFault.

# Inputs are the galaxy name (folder) and whether to use the contsub
# HI version or not

export script_path=${HOME}/ownCloud/code_development/

# NGC 205 w/ and w/o contsub
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 y 1

# Run in 3 stages
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 1 natural 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 1 natural 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 1 natural 3


# w/o contsub
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 n 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 False 1 natural 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 False 1 natural 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 False 1 natural 3


# briggs w/ 2 km/s channels
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 y 5
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 briggs 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 briggs 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 briggs 3

# Uniform w/ 2 km/s channels
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 y 5
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 uniform 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 uniform 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 True 5 uniform 3


# NGC 185 w/ and w/o contsub
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 y 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 1 natural 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 1 natural 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 1 natural 3

# With large 4.8 km/s channels
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 12 natural 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 12 natural 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 12 natural 3

# w/o contsub
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 y 5
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 False 1 natural 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 False 1 natural 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 False 1 natural 3

# briggs w/ 3 km/s channels
# $HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 4 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 n 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 briggs 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 briggs 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 briggs 3

# # Uniform w/ 3 km/s channels
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 uniform 1
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 uniform 2
$HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 True 8 uniform 3