
# Run concat_channels.py to make the 14A cubes

code_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA/scripts/'

cd HI_contsub_0_42kms

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_14A_HI_contsub_width_04kms 1526 image
# remove partial imgs
rm -r images/M31_14A_HI_contsub_width_04kms.image_*

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_14A_HI_contsub_width_04kms 1526 pb
# rm -r pbs/M31_14A_HI_contsub_width_04kms.pb_*

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_14A_HI_contsub_width_04kms 1526 residual
rm -r residuals/M31_14A_HI_contsub_width_04kms.residual_*

# Make pbcor image
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/run_impbcor.py images/M31_14A_HI_contsub_width_04kms.image pbs/M31_14A_HI_contsub_width_04kms.pb


# Make FITS
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py images/M31_14A_HI_contsub_width_04kms.image
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py images/M31_14A_HI_contsub_width_04kms.image.pbcor
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py residuals/M31_14A_HI_contsub_width_04kms.residual
~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/export_to_fits.py pbs/M31_14A_HI_contsub_width_04kms.pb

# Copy the FITS into their final place in bigdata
fits_dir='/home/ekoch/bigdata/ekoch/M31/VLA/14A-235/HI/full_imaging_noSD'
mkdir $fits_dir
mv images/M31_14A_HI_contsub_width_04kms.image.fits $fits_dir/
mv images/M31_14A_HI_contsub_width_04kms.image.pbcor.fits $fits_dir/
mv residuals/M31_14A_HI_contsub_width_04kms.residual.fits $fits_dir/
mv pbs/M31_14A_HI_contsub_width_04kms.pb.fits $fits_dir/

cd ../


# cd HI_contsub_1_26kms

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 image

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 pb

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 residual

# cd ../
