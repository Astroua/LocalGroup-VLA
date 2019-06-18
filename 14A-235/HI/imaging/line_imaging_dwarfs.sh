# Not a cluster submission script! Run on SegFault.

# Inputs are the galaxy name (folder) and whether to use the contsub
# HI version or not

export script_path=${HOME}/ownCloud/code_development/

# NGC 205 w/ and w/o contsub
$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 y 1

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 n 1

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC205 y 5

# NGC 185 w/ and w/o contsub
$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 y 1

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 y 5

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 4 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $script_path/LocalGroup-VLA/14A-235/HI/imaging/line_imaging_dwarfs.py NGC185 n 1