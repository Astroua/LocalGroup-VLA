#!/bin/bash
#SBATCH --time=16:00:00
#SBATCH --mem=128000M
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --job-name=M31_15A-HI_match_and_combine-%A-%a
#SBATCH --output=casa-m31-15A_HI_match_and_combine-%A-%a.out
#SBATCH --array=0-5%1

# Each job copies the whole MS to the node storage, then splits out 1/18th of the total channels
# and copies back to scratch

export OMP_NUM_THREADS=$SLURM_JOB_CPUS_PER_NODE

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

export scratch_path=/home/ekoch/scratch/M31_imaging/15A-175/

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

export out_chan_folder="HI_contsub_0_42kms"

echo "Copy whole MS to node"
cp -r $scratch_path/15A-175_Btracks_HI_spw_0_LSRK.ms.contsub .
cp -r $scratch_path/15A-175_Ctracks_HI_spw_0_LSRK.ms.contsub .
cp -r $scratch_path/M31_14A-235_15Afields_HI_spw_0_LSRK_freqmatch.ms.contsub .
# Enable to do non contsub version
# cp -r $scratch_path/M31_14A-235_HI_spw_0_LSRK.ms .

mkdir ${out_chan_folder}

casa-release-5.4.1-32.el7/bin/mpicasa -n 32 casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/code/LocalGroup-VLA/15A-175/HI/imaging/match_and_split.py True 1.26 $job_num 6 ${scratch_path}/${out_chan_folder}/

# echo "Copy back to scratch"
# cp -r ${out_chan_folder}/* ${scratch_path}/${out_chan_folder}/

# Local run example
# ~/casa-release-5.4.1-32.el7/bin/casa --nologger --nogui --log2term --nocrashreport -c $HOME/ownCloud/code_development/LocalGroup-VLA/15A-175/HI/imaging/match_and_split.py True 1.26 0 6 .

echo "DONE ${job_num}!"
