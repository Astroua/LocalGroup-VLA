#!/bin/bash

# export repo_path='${HOME}/code/LocalGroup-VLA'
export repo_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA'

for gal in {"WLM","NGC6822","SextansA","IC1613"}; do
    ${HOME}/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c ${repo_path}/13A-213/imaging/transform_and_uvsub.py $gal
done