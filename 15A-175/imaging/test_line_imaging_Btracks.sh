#!/bin/bash
#SBATCH --time=124:00:00
#SBATCH --mem=1547000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=M31_15A_Btracks_dirty_cube-%A-%a
#SBATCH --output=casa-m31_15A_Btracks_dirtycube-%A-%a.out
#SBATCH --array=0,2-4%1

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

# Give which spw using the --export flag when calling sbatch
export scratch_path=/home/ekoch/scratch/M31_imaging/15A-175/

# export project_path=/home/ekoch/project/ekoch/

# Move to scratch space b/c casa write out the temporary files into the same folder
cd $scratch_path

Xvfb :1 &
export DISPLAY=:1

spw=$SLURM_ARRAY_TASK_ID

echo "OMP_NUM_THREADS "$OMP_NUM_THREADS
echo "Running SPW "$spw

$HOME/casa-release-5.5.0-149.el7/bin/mpicasa -n 32 $HOME/casa-release-5.5.0-149.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/15A-175/imaging/test_line_imaging_Btracks.py $spw

# Copy the dirty_cube folder into project space
# cp -R $scratch_path/dirty_cube $project_path
