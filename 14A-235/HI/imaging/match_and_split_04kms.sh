#!/bin/bash
#SBATCH --time=16:00:00
#SBATCH --mem=128000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=M31_14A-HI_match_and_combine-%A-%a
#SBATCH --output=casa-m31-14A_HI_match_and_combine-%A-%a.out
#SBATCH --array=0-17%1

# Each job copies the whole MS to the node storage, then splits out 1/18th of the total channels
# and copies back to scratch

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

export scratch_path=/home/ekoch/scratch/M31_imaging/14A-235/

job_num=$SLURM_ARRAY_TASK_ID

# CASA runs better if each job has it's own source files
# So we'll run from the node storage
tmp_dir=$SLURM_TMPDIR/concat_M33_chans_1kms_${suffix_arr[$job_num]}
mkdir $tmp_dir

cd $tmp_dir

export casa_scratch_path="$HOME/scratch/casa-release-5.4.1-32.el7"

cp -r $casa_scratch_path .

# Copy the init file
mkdir .casa
cp $HOME/.casa/init.py .casa/

rc_path="${tmp_dir}/.casa"

Xvfb :1 &
export DISPLAY=:1

echo "Copy whole MS to node"
cp -r $scratch_path/M31_14A-235_HI_spw_0_LSRK.ms.contsub .
mkdir HI_contsub_0_42kms

# Enable to do non contsub version
# cp -r $scratch_path/M31_14A-235_HI_spw_0_LSRK.ms .

casa-release-5.4.1-32.el7/bin/mpicasa -n 32 casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/14A-235/HI/imaging/match_and_split.py True 0.42 $job_num 18

echo "Copy back to scratch"
cp -r HI_contsub_0_42kms/* ${scratch_path}/HI_contsub_0_42kms/

echo "DONE ${job_num}!"
