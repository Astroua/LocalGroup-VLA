
# This will create concatenated per-SPW ms w/ only the
# target fields and dirty maps for each SPW.

# export repo_path='${HOME}/code/LocalGroup-VLA'
export repo_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA'

for gal in {"WLM","NGC6822","SextansA","IC1613"}; do

    for (( spw = 0; spw < 12; spw++ )); do
    	$HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c ${repo_path}/13A-213/imaging/test_line_imaging.py ${gal} $spw
    done

done
