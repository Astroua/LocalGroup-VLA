
# Run concat_channels.py to make the 15A cubes

code_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA/scripts/'

cd HI_contsub_0_42kms

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 image
# remove partial imgs
rm -r images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image_*

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 pb
rm -r pbs/M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb_*

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 residual
rm -r residuals/M31_15A_B_C_14A_HI_contsub_width_0_4kms.residual_*

# Make pbcor image
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/run_impbcor.py images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image pbs/M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb


# Make FITS
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py residuals/M31_15A_B_C_14A_HI_contsub_width_0_4kms.residual
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py pbs/M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb

# Copy the FITS into their final place in bigdata
fits_dir='/home/ekoch/bigdata/ekoch/M31/VLA/15A-175/HI/full_imaging_BCD_taper_0_42kms_noSD'
mkdir $fits_dir
mv images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.fits $fits_dir/
mv images/M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.pbcor.fits $fits_dir/
mv residuals/M31_15A_B_C_14A_HI_contsub_width_0_4kms.residual.fits $fits_dir/
mv pbs/M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits $fits_dir/

cd ../

# Run feather comparisons
# Scripts to be run from the repo dir.
code_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA/'

cd $code_path

# Run with ipython b/c I (EWK) have a startup script that adds
# the LocalGroup-VLA repo to the python path

# Make matched versions of the SD to the VLA cube
ipython ${code_path}/15A-175/HI/imaging/ebhis_regrid_m31.py

# Check uv-overlap properties before feathering
ipython ${code_path}/15A-175/HI/imaging/feather_comparisons.py

# Now do the feathering
# CHANGE THE SD CORRECTION FACTOR BASED ON feather_comparisons.py
# (i.e., don't blindly feather the cubes)
ipython ${code_path}/15A-175/HI/imaging/feather_cubes.py

# Check flux recovery per-channel between VLA, VLA+SD, and SD
ipython ${code_path}/15A-175/HI/imaging/check_flux_recovery.py

# Make a signal mask and moment maps.
ipython ${code_path}/15A-175/HI/analysis/cube_pipeline.py


cd HI_contsub_1_26kms

# Stage 1 cubes for inspection
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images_stage1/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 262 image

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals_stage1/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 262 residuals

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 262 pb

# Final images and residuals
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 262 image

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 262 residual


# cd ../
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/run_impbcor.py M31_15A_B_C_14A_HI_contsub_width_1_2kms.image M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb


# Make FITS
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py M31_15A_B_C_14A_HI_contsub_width_1_2kms.image
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py M31_15A_B_C_14A_HI_contsub_width_1_2kms.residual
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb

fits_dir='/home/ekoch/bigdata/ekoch/M31/VLA/15A-175/HI/full_imaging_1_2kms_noSD/'
mkdir $fits_dir
mv M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.fits $fits_dir/
mv M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.pbcor.fits $fits_dir/
mv M31_15A_B_C_14A_HI_contsub_width_1_2kms.residual.fits $fits_dir/
mv M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits $fits_dir/

# Feathering and masking scripts.
# Note that the 1.2 km/s settings need to be enabled in the
# scripts for this to work
ipython ${code_path}/15A-175/HI/imaging/ebhis_regrid_m31.py

# Check uv-overlap properties before feathering
ipython ${code_path}/15A-175/HI/imaging/feather_comparisons.py

# Now do the feathering
# CHANGE THE SD CORRECTION FACTOR BASED ON feather_comparisons.py
# (i.e., don't blindly feather the cubes)
ipython ${code_path}/15A-175/HI/imaging/feather_cubes.py

# Check flux recovery per-channel between VLA, VLA+SD, and SD
ipython ${code_path}/15A-175/HI/imaging/check_flux_recovery.py

# Make a signal mask and moment maps.
ipython ${code_path}/15A-175/HI/analysis/cube_pipeline.py
