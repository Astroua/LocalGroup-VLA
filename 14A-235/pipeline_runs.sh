
# Setup pipeline directories for each MS
# Run only line SPWs for now

# Raw data live on rubin. Copy over when running
# the track
export raw_data_path='/home/koch.473/rubin/VLA_tracks/14A-235/reduction/'

export track_folder='14A-235_07_17_14'
export track_name='14A-235.sb29371209.eb29491483.56855.45020903935'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_18_14'
export track_name='14A-235.sb29418542.eb29492706.56856.28926070602'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

# export track_folder='14A-235_07_20_14'
# export track_name='14A-235.sb29371209.eb29502506.56858.460165509256'

# mkdir $track_folder
# mv "${raw_data_path}/${track_name}.tar" $track_folder
# cd $track_folder
# tar -xf "${track_name}.tar"
# ~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# # Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
# cd "${track_folder}_speclines"
# ~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
# cd ../../

export track_folder='14A-235_07_25_14'
export track_name='14A-235.sb29418542.eb29508034.56863.29090856481'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_26_14'
export track_name='14A-235.sb29418542.eb29508731.56864.28173256945'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_27_14'
export track_name='14A-235.sb29371209.eb29509155.56865.36711972222'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# # Save space by removing intermediate products
# rm -f "${track_name}.tar"
rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_28_14'
export track_name='14A-235.sb29418542.eb29509243.56866.32426545139'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_29_14'
export track_name='14A-235.sb29418542.eb29509553.56867.32148467592'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_31_14_early'
export track_name='14A-235.sb29418542.eb29511902.56869.30431443287'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_07_31_14_late'
export track_name='14A-235.sb29371209.eb29511924.56869.44281552083'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_08_02_14'
export track_name='14A-235.sb29418542.eb29513453.56871.3237440625'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_08_04_14'
export track_name='14A-235.sb29371209.eb29514731.56873.33214849537'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_08_08_14'
export track_name='14A-235.sb29371209.eb29573515.56877.400355289356'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

# export track_folder='14A-235_08_09_14'
# export track_name='14A-235.sb29418542.eb29584935.56878.23325265046'

# mkdir $track_folder
# mv "${raw_data_path}/${track_name}.tar" $track_folder
# cd $track_folder
# tar -xf "${track_name}.tar"
# ~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# # Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
# cd "${track_folder}_speclines"
# ~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
# cd ../../

# export track_folder='14A-235_08_10_14'
# export track_name='14A-235.sb29371560.eb29585086.56879.480768125'

# mkdir $track_folder
# mv "${raw_data_path}/${track_name}.tar" $track_folder
# cd $track_folder
# tar -xf "${track_name}.tar"
# ~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# # Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
# cd "${track_folder}_speclines"
# ~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
# cd ../../

# export track_folder='14A-235_08_11_14_early'
# export track_name='14A-235.sb29418542.eb29585096.56880.26525332176'

# mkdir $track_folder
# mv "${raw_data_path}/${track_name}.tar" $track_folder
# cd $track_folder
# tar -xf "${track_name}.tar"
# ~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# # Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
# cd "${track_folder}_speclines"
# ~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
# cd ../../

# 08_11_14 is split into 2. May have failed for other reasons, too
# export track_folder='14A-235_08_11_14_late'
# export track_name='bandboard.56880.69633658565
# bandboard_000.56880.69749452546	'

# mkdir $track_folder
# mv "${raw_data_path}/${track_name}.tar" $track_folder
# cd $track_folder
# tar -xf "${track_name}.tar"
# ~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
#rm -f "${track_name}.tar"
#rm -rf "${track_name}.ms"*
# cd "${track_folder}_speclines"
# ~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
# cd ../../

export track_folder='14A-235_08_15_14'
export track_name='14A-235.sb29371560.eb29588511.56884.49103833333'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_08_17_14'
export track_name='14A-235.sb29371560.eb29589770.56886.467028680556'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../

export track_folder='14A-235_08_21_14'
export track_name='14A-235.sb29590027.eb29596487.56890.46132725694'

mkdir $track_folder
mv "${raw_data_path}/${track_name}.tar" $track_folder
cd $track_folder
tar -xf "${track_name}.tar"
~/casa-release-5.4.1-32.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/ms_split.py $track_name F lines
# Save space by removing intermediate products
# rm -f "${track_name}.tar"
# rm -rf "${track_name}.ms"*
cd "${track_folder}_speclines"
~/casa-release-5.4.1-32.el6/bin/casa --pipeline --nogui --log2term -c ~/LocalGroup-VLA/14A-235/pipeline_scripts/casa_pipeline_lines.py "${track_name}.speclines.ms"
cd ../../


# Backups onto kant
export backup_loc="/home/koch.473/kant/VLA_tracks/14A-235/pipeline_products"

cd 14A-235_07_17_14/14A-235_07_17_14_speclines
cp -r products $backup_loc/14A-235_07_17_14
cd ../..
cd 14A-235_07_18_14/14A-235_07_18_14_speclines
cp -r products $backup_loc/14A-235_07_18_14
cd ../..
# cd 14A-235_07_20_14/14A-235_07_20_14_speclines
# cp -r products $backup_loc/14A-235_07_20_14
# cd ../..
cd 14A-235_07_25_14/14A-235_07_25_14_speclines
cp -r products $backup_loc/14A-235_07_25_14
cd ../..
cd 14A-235_07_26_14/14A-235_07_26_14_speclines
cp -r products $backup_loc/14A-235_07_26_14
cd ../..
cd 14A-235_07_27_14/14A-235_07_27_14_speclines
cp -r products $backup_loc/14A-235_07_27_14
cd ../..
cd 14A-235_07_28_14/14A-235_07_28_14_speclines
cp -r products $backup_loc/14A-235_07_28_14
cd ../..
cd 14A-235_07_29_14/14A-235_07_29_14_speclines
cp -r products $backup_loc/14A-235_07_29_14
cd ../..
cd 14A-235_07_31_14_early/14A-235_07_31_14_early_speclines
cp -r products $backup_loc/14A-235_07_31_14_early
cd ../..
cd 14A-235_07_31_14_late/14A-235_07_31_14_late_speclines
cp -r products $backup_loc/14A-235_07_31_14_late
cd ../..
cd 14A-235_08_02_14/14A-235_08_02_14_speclines
cp -r products $backup_loc/14A-235_08_02_14
cd ../..
cd 14A-235_08_04_14/14A-235_08_04_14_speclines
cp -r products $backup_loc/14A-235_08_04_14
cd ../..
cd 14A-235_08_08_14/14A-235_08_08_14_speclines
cp -r products $backup_loc/14A-235_08_08_14
cd ../..
# cd 14A-235_08_09_14/14A-235_08_09_14_speclines
# cp -r products $backup_loc/14A-235_08_09_14
# cd ../..
# cd 14A-235_08_10_14/14A-235_08_10_14_speclines
# cp -r products $backup_loc/14A-235_08_10_14
# cd ../..
# cd 14A-235_08_11_14_early/14A-235_08_11_14_early_speclines
# cp -r products $backup_loc/14A-235_08_11_14_early
# cd ../..
# cd 14A-235_08_11_14_late/14A-235_08_11_14_late_speclines
# cp -r products $backup_loc/14A-235_08_11_14_late
cd ../..
cd 14A-235_08_15_14/14A-235_08_15_14_speclines
cp -r products $backup_loc/14A-235_08_15_14
cd ../..
cd 14A-235_08_17_14/14A-235_08_17_14_speclines
cp -r products $backup_loc/14A-235_08_17_14
cd ../..
cd 14A-235_08_21_14/14A-235_08_21_14_speclines
cp -r products $backup_loc/14A-235_08_21_14
cd ../..

# Move calibrated MS to own directory

export export_data_path='/home/koch.473/VLA_tracks/14A-235/'

cd 14A-235_07_17_14/14A-235_07_17_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_18_14/14A-235_07_18_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_25_14/14A-235_07_25_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_26_14/14A-235_07_26_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_27_14/14A-235_07_27_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_28_14/14A-235_07_28_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_29_14/14A-235_07_29_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_31_14_early/14A-235_07_31_14_early_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_07_31_14_late/14A-235_07_31_14_late_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_02_14/14A-235_08_02_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_04_14/14A-235_08_04_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_08_14/14A-235_08_08_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_15_14/14A-235_08_15_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_17_14/14A-235_08_17_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
cd 14A-235_08_21_14/14A-235_08_21_14_speclines/
mv 14A-235*.speclines.ms $export_data_path/
cd ../..
