#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --mem=128000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=M31_15A_concat_split-%A-%a
#SBATCH --output=casa-m31_15A_concat_split-%A-%a.out
#SBATCH --array=0,1

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

export scratch_path=/home/ekoch/scratch/M31_imaging/15A-175/

# Move to scratch space b/c casa write out the temporary files into the same folder
cd $scratch_path

Xvfb :1 &
export DISPLAY=:1

# Treat the B and C config tracks separately
export track_num=$SLURM_ARRAY_TASK_ID

$HOME/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/15A-175/imaging/concat_and_split.py $track_num
