#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --mem=512000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=M31_11B_stage1clean_cube-%J
#SBATCH --output=casa-m31_11B_stage1clean_cube-%J.out
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


Xvfb :1 &
export DISPLAY=:1

echo "OMP_NUM_THREADS "$OMP_NUM_THREADS
echo "Running SPW "$spw

$HOME/casa-release-5.4.1-32.el7/bin/mpicasa -n 32 $HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/11B-124/imaging/line_imaging_stage1.py $gal_folder

# Copy the dirty_cube folder into project space
# cp -R $scratch_path/dirty_cube $project_path
