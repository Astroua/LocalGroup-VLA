
# Run from /home/koch.473/kant/13A-213

# This will create concatenated per-SPW ms w/ only the
# target fields and dirty maps for each SPW.

# IC 1613

for (( spw = 0; spw < 12; spw++ )); do
	$HOME/casa-release-5.4.1-32.el6/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/LocalGroup-VLA/13A-213/imaging/test_line_imaging.py IC1613 $spw
done

# WLM

for (( spw = 0; spw < 12; spw++ )); do
	$HOME/casa-release-5.4.1-32.el6/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/LocalGroup-VLA/13A-213/imaging/test_line_imaging.py WLM $spw
done

# Sextans A

for (( spw = 0; spw < 12; spw++ )); do
	$HOME/casa-release-5.4.1-32.el6/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/LocalGroup-VLA/13A-213/imaging/test_line_imaging.py SextansA $spw
done

# NGC6822

for (( spw = 0; spw < 12; spw++ )); do
	$HOME/casa-release-5.4.1-32.el6/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/LocalGroup-VLA/13A-213/imaging/test_line_imaging.py NGC6822 $spw
done
