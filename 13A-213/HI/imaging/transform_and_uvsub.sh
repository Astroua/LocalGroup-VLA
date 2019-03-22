#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --mem=128000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=13A_HI_transform_and_uvsub-%A-%a
#SBATCH --output=casa-13A_HI_transform_and_uvsub-%A-%a.out
#SBATCH --array=0-3

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

export scratch_path=/home/ekoch/scratch/13A-213_imaging/

# Job numbers correspond to the 4 diff. galaxies
job_num=$SLURM_ARRAY_TASK_ID

if [[ $job_num -eq 0 ]]; then
    gal_folder='NGC6822'
elif [[ $job_num -eq 1 ]]; then
    gal_folder='WLM'
elif [[ $job_num -eq 2 ]]; then
    gal_folder='IC1613'
elif [[ $job_num -eq 3 ]]; then
    gal_folder='SextansA'
fi

# Move to scratch space b/c casa write out the temporary files into the same folder
cd $scratch_path/$gal_folder

Xvfb :1 &
export DISPLAY=:1

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 32 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/11B-124/imaging/transform_and_uvsub.py $gal_folder
