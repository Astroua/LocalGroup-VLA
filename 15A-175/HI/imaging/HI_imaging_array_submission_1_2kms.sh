#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --mem=128000M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --job-name=M31_15A_1_2kms-%A-%a
#SBATCH --output=casa-M31_15A_1_2kms-%A-%a.out
#SBATCH --array=0-65

# Use array to set which channels will get imaged.
# Run from a separate folder so the log files are in one place.

module restore my_default

source /home/ekoch/.bashrc
source /home/ekoch/preload.bash

job_num=$SLURM_ARRAY_TASK_ID

# Build in a slight offset for each job to avoid starting a bunch of CASA
# sessions at once
# sleep $(($job_num + 30))

# Move to scratch space b/c casa write out the temporary files into the same folder
export scratch_path=/home/ekoch/scratch/M31_imaging/15A-175/

cd $scratch_path

Xvfb :1 &
export DISPLAY=:1

# Set which imaging stage to run: the initial 5-sigma clean (1) or the full clean with a mask to (2)
stage=1

if (( $stage==1 )); then
    script_name="${HOME}/code/LocalGroup-VLA/15A-175/HI/imaging/HI_single_channel_clean.py"
    # Parameter file for tclean
    param_file="/home/ekoch/code/LocalGroup-VLA/15A-175/HI/imaging/param_files/15A_B_C_14A_1_2kms.saved"
elif (( $stage==2 )); then
    script_name="${HOME}/code/LocalGroup-VLA/15A-175/HI/imaging/HI_single_channel_clean_stage2.py"
    param_file="/home/ekoch/code/LocalGroup-VLA/15A-175/HI/imaging/param_files/15A_B_C_14A_1_2kms_stage2.saved"
else
    echo "Stage must be 1 or 2, not ${stage}".
    exit 1
fi

# Start 5 channels running on the node
# This is well-suited for the cedar base nodes
start_chan=$(($job_num * 4))
end_chan=$((($job_num + 1) * 4))

# Path to the casa files
export casa_scratch_path="$HOME/scratch/casa-release-5.4.1-32.el7"

export chan_path_name="HI_contsub_1_26kms"

# B/c CASA spawns other processes internally, and if something crashes in the scripts,
# the wait command may hang until the job is killed
# Try recording the casa interpreter PIDs and only make wait subject to those.
pids=

for (( chan_num = $start_chan; chan_num < $end_chan; chan_num++ )); do

    echo "Running channel "$chan_num

    # Make a new directory on the node storage
    tmp_dir=$SLURM_TMPDIR/run_chan_${chan_num}
    mkdir $tmp_dir

    cd $tmp_dir

    # Move the data to the temp path
    mkdir ${chan_path_name}
    mkdir ${chan_path_name}/channel_${chan_num}
    cp -r $scratch_path/${chan_path_name}/channel_${chan_num}/* ${chan_path_name}/channel_${chan_num}/

    # Copy a new casa instance to avoid slower i/o on scratch or in home
    cp -r $casa_scratch_path .

    # Copy the init file
    mkdir .casa
    cp $HOME/.casa/init.py .casa/

    rc_path="${tmp_dir}/.casa"

    (casa-release-5.4.1-32.el7/bin/mpicasa -n 8 casa-release-5.4.1-32.el7/bin/casa --rcdir ${rc_path} --nologger --nogui --logfile $scratch_path/${chan_path_name}/casa_M31_HI_15A_12kms_${chan_num}_${SLURM_JOB_ID}_$(date "+%Y%m%d-%H%M%S")_stage${stage}.log --nocrashreport -c $script_name $chan_num $param_file "${chan_path_name}"; cp -r ${chan_path_name}/channel_${chan_num}/* $scratch_path/${chan_path_name}/channel_${chan_num}/) &
    pids+=" $!"

    cd $tmp_dir

    sleep 5

done

wait $pids || { echo "There was an error" >&2; exit 1; }

echo "All CASA jobs exited."
