
# Setup pipeline directories for each MS
# Run only line SPWs for now

# Raw data live on rubin. Copy over when running
# the track
export raw_data_path='/home/koch.473/rubin/VLA_tracks/15A-175/reduction/'

export track_folder='15A-175_02_08_15'
export track_name='15A-175.sb30134708.eb30356819.57061.020229120375'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_09_15'
export track_name='15A-175.sb30134708.eb30359405.57062.017486770834'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_16_15'
export track_name='15A-175.sb30134512.eb30434584.57069.80891486111'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_18_15'
export track_name='15A-175.sb30134708.eb30438824.57071.02339746528'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_21_15_early'
export track_name='15A-175.sb30134512.eb30449005.57074.75357318287'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_21_15_late'
export track_name='15A-175.sb30134512.eb30449006.57074.83387934028'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_23_15'
export track_name='15A-175.sb30134412.eb30449392.57076.002348842594'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_24_15'
export track_name='15A-175.sb30134708.eb30452819.57077.97151658565'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_03_07_15'
export track_name='15A-175.sb30134610.eb30471894.57088.77506327546'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_03_14_15'
export track_name='15A-175.sb30134610.eb30477274.57095.794690254625'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_05_01_15'
export track_name='15A-175.sb30134412.eb30634371.57143.8107067824'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_05_08_15'
export track_name='15A-175.sb30650468.eb30663700.57150.77433534722'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_01_29_16'
export track_name='15A-175.sb31621972.eb31740192.57416.862559490735'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_01_30_16'
export track_name='15A-175.sb31621972.eb31744602.57417.81571539352'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_02_16'
export track_name='15A-175.sb31621836.eb31763442.57420.090581944445'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_05_16'
export track_name='15A-175.sb31622106.eb31808960.57423.916207013885'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_15_16_early'
export track_name='15A-175.sb31622324.eb31851993.57433.03848378472'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
Save space by removing intermediate products
rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_15_16_late'
export track_name='15A-175.sb31622106.eb31853922.57433.87005864583'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_16_16_early'
export track_name='15A-175.sb31622324.eb31853924.57434.015447881946'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_16_16_late'
export track_name='15A-175.sb31622324.eb31856949.57434.99643854167'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_18_16'
export track_name='15A-175.sb31622324.eb31864321.57436.01421613426'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_19_16'
export track_name='15A-175.sb31621836.eb31869270.57437.00218548611'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='15A-175_02_20_16'
export track_name='15A-175.sb31622106.eb31870283.57438.81578400463'

mkdir $track_folder
mv "${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/kant/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}."*
cd "${track_folder}_speclines"
~/kant/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/15A-175/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

# Backups onto kant
export backup_loc="/home/koch.473/kant/VLA_tracks/15A-175/pipeline_products"

cd 15A-175_02_08_15
cp -r products $backup_loc/15A-175_02_08_15
cd ..
cd 15A-175_02_09_15
cp -r products $backup_loc/15A-175_02_09_15
cd ..
cd 15A-175_02_16_15
cp -r products $backup_loc/15A-175_02_16_15
cd ..
cd 15A-175_02_18_15
cp -r products $backup_loc/15A-175_02_18_15
cd ..
cd 15A-175_02_21_15_early
cp -r products $backup_loc/15A-175_02_21_15_early
cd ..
cd 15A-175_02_21_15_late
cp -r products $backup_loc/15A-175_02_21_15_late
cd ..
cd 15A-175_02_23_15
cp -r products $backup_loc/15A-175_02_23_15
cd ..
cd 15A-175_02_24_15
cp -r products $backup_loc/15A-175_02_24_15
cd ..
cd 15A-175_03_07_15
cp -r products $backup_loc/15A-175_03_07_15
cd ..
cd 15A-175_03_14_15
cp -r products $backup_loc/15A-175_03_14_15
cd ..
cd 15A-175_05_01_15
cp -r products $backup_loc/15A-175_05_01_15
cd ..
cd 15A-175_05_08_15
cp -r products $backup_loc/15A-175_05_08_15
cd ..
cd 15A-175_01_29_16
cp -r products $backup_loc/15A-175_01_29_16
cd ..
cd 15A-175_01_30_16
cp -r products $backup_loc/15A-175_01_30_16
cd ..
cd 15A-175_02_02_16
cp -r products $backup_loc/15A-175_02_02_16
cd ..
cd 15A-175_02_05_16
cp -r products $backup_loc/15A-175_02_05_16
cd ..
cd 15A-175_02_15_16_early
cp -r products $backup_loc/15A-175_02_15_16_early
cd ..
cd 15A-175_02_15_16_late
cp -r products $backup_loc/15A-175_02_15_16_late
cd ..
cd 15A-175_02_16_16_early
cp -r products $backup_loc/15A-175_02_16_16_early
cd ..
cd 15A-175_02_16_16_late
cp -r products $backup_loc/15A-175_02_16_16_late
cd ..
cd 15A-175_02_18_16
cp -r products $backup_loc/15A-175_02_18_16
cd ..
cd 15A-175_02_19_16
cp -r products $backup_loc/15A-175_02_19_16
cd ..
cd 15A-175_02_20_16
cp -r products $backup_loc/15A-175_02_20_16
cd ..

# Move speclines tracks to a single folder

export calibrated_folder='/home/koch.473/kant/'
