
# Run concat_channels.py to make the 15A cubes

code_path='/home/ekoch/ownCloud/code_development/LocalGroup-VLA/15A-175/HI/imaging/'

cd HI_contsub_0_42kms

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 image

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 pb

~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_15A_B_C_14A_HI_contsub_width_0_4kms 762 residual

cd ../


# cd HI_contsub_1_26kms

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py images/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 image

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py pbs/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 pb

# ~/casa-release-5.5.0-149.el7/bin/casa --log2term --nogui -c $code_path/concat_channels.py residuals/ M31_15A_B_C_14A_HI_contsub_width_1_2kms 762 residual

# cd ../
