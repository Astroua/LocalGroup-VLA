#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --mem=128000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=13A_stage1clean_cube-%A-%a
#SBATCH --output=casa-13A_stage1clean_cube-%A-%a.out
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

cd $scratch_path/$gal_folder

Xvfb :1 &
export DISPLAY=:1

echo "OMP_NUM_THREADS "$OMP_NUM_THREADS
echo "Running SPW "$spw

# Inputs are the galaxy name (folder) and whether to use the contsub
# HI version or not

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 32 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/13A-213/HI/imaging/line_imaging_stage1.py $gal_folder y
