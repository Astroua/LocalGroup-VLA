
# Setup pipeline directories for each MS

mkdir 11B-124_10_17_11
mv 11B-124.sb5338463.eb5670977.55851.2071834838.tar 11B-124_10_17_11
cd 11B-124_10_17_11
tar -xf 11B-124.sb5338463.eb5670977.55851.2071834838.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5338463.eb5670977.55851.2071834838 n n

cd ..

mkdir 11B-124_11_02_11
mv 11B-124.sb5334017.eb5769266.55867.351589467595.tar 11B-124_11_02_11
cd 11B-124_11_02_11
tar -xf 11B-124.sb5334017.eb5769266.55867.351589467595.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5769266.55867.351589467595 n n

cd ..

mkdir 11B-124_11_03_11
mv 11B-124.sb5334017.eb5770285.55868.35039530093.tar 11B-124_11_03_11
cd 11B-124_11_03_11
tar -xf 11B-124.sb5334017.eb5770285.55868.35039530093.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5770285.55868.35039530093 n n

cd ..

mkdir 11B-124_11_07_11
mv 11B-124.sb5334017.eb5794981.55872.243100023145.tar 11B-124_11_07_11
cd 11B-124_11_07_11
tar -xf 11B-124.sb5334017.eb5794981.55872.243100023145.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5794981.55872.243100023145 n n

cd ..

mkdir 11B-124_11_10_11
mv 11B-124.sb5334017.eb5886098.55875.214899375.tar 11B-124_11_10_11
cd 11B-124_11_10_11
tar -xf 11B-124.sb5334017.eb5886098.55875.214899375.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5886098.55875.214899375 n n

cd ..

mkdir 11B-124_11_14_11
mv 11B-124.sb5334017.eb5925791.55879.318273530094.tar 11B-124_11_14_11
cd 11B-124_11_14_11
tar -xf 11B-124.sb5334017.eb5925791.55879.318273530094.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5925791.55879.318273530094 n n

cd ..

mkdir 11B-124_11_15_11
mv 11B-124.sb5334017.eb5931951.55880.295246284724.tar 11B-124_11_15_11
cd 11B-124_11_15_11
tar -xf 11B-124.sb5334017.eb5931951.55880.295246284724.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5931951.55880.295246284724 n n

cd ..

mkdir 11B-124_11_18_11
mv 11B-124.sb5334017.eb5943937.55883.286567627314.tar 11B-124_11_18_11
cd 11B-124_11_18_11
tar -xf 11B-124.sb5334017.eb5943937.55883.286567627314.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5943937.55883.286567627314 n n

cd ..

mkdir 11B-124_11_21_11
mv 11B-124.sb5334017.eb5945548.55886.29915828704.tar 11B-124_11_21_11
cd 11B-124_11_21_11
tar -xf 11B-124.sb5334017.eb5945548.55886.29915828704.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5945548.55886.29915828704 n n

cd ..

mkdir 11B-124_11_22_11
mv 11B-124.sb5334017.eb5952572.55887.25485887731.tar 11B-124_11_22_11
cd 11B-124_11_22_11
tar -xf 11B-124.sb5334017.eb5952572.55887.25485887731.tar
~/casa-release-5.0.0-218.el6/bin/casa --nogui --log2term -c ~/LocalGroup-VLA/11B-124/pipeline5.0.0/EVLA_pipeline.py 11B-124.sb5334017.eb5952572.55887.25485887731 n n

cd ..

# Backups onto kant
export backup_loc="/home/koch.473/kant/VLA_tracks/11B-124/pipeline_products"

cd 11B-124_10_17_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_02_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_03_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_07_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_10_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_14_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_15_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_18_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_21_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
cd 11B-124_11_22_11
~/anaconda3/bin/python ~/LocalGroup-VLA/script_pipeline_backup.py $backup_loc
cd ../
