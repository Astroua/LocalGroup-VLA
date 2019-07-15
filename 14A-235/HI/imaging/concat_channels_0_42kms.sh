#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --mem=4000M
#SBATCH --ntasks=1
#SBATCH --job-name=M31_14A_HI_concat_channel-042kms-%A-%a
#SBATCH --output=casa-m31_14A_HI_concat_channel-042kms-%A-%a.out
#SBATCH --array=0-9

# Combine the imaged channels into cubes
# Run on whole node for the memory.

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

export scratch_path=/home/ekoch/scratch/M31_imaging/14A-235/

num_chans=1526

# Move to scratch space b/c casa write out the temporary files into the same folder
# cd $scratch_path

Xvfb :1 &
export DISPLAY=:1

suffixes="mask model pb psf residual residual_init image sumwt weight"
suffix_arr=($suffixes)

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

# Now copy all of the images to the node storage
mkdir HI_contsub_0_42kms_${suffix_arr[$job_num]}
for i in {0..1525}; do
    cp -r $scratch_path/HI_contsub_0_42kms/channel_${i}/*.${suffix_arr[$job_num]} HI_contsub_0_42kms_${suffix_arr[$job_num]}/
    # echo "Copied channel ${i}"
done

echo "Concatenating channels"
casa-release-5.4.1-32.el7/bin/casa --rcdir ${rc_path} --nologger --nogui --log2term --nocrashreport -c $HOME/code/VLA_Lband/17B-162/HI/imaging/concat_channels.py "HI_contsub_0_42kms_${suffix_arr[$job_num]}" "M31_14A_HI_contsub_width_04kms" $num_chans ${suffix_arr[$job_num]}

echo "Copying M31_14A-235_HI_contsub_width_0_42kms.${suffix_arr[$job_num]} to scratch"
cp -r HI_contsub_0_42kms_${suffix_arr[$job_num]} $scratch_path/

echo "Done!"