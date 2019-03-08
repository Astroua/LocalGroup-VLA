
'''
Create a zipped tar file of the scripted pipeline products
and copy it into a backed-up location.

Run from the directory with the pipeline outputs.
'''

import os
import sys
from distutils.dir_util import copy_tree
import tarfile
from glob import glob

backup_location = sys.argv[1]

products_folder = 'products'
if not os.path.exists(products_folder):
    os.mkdir(products_folder)
else:
    os.system("rm -rf {}".format(products_folder))

# Copy the weblog, pipeline_restore, caltables, and
# flagversions to the new folder

copy_tree("weblog", os.path.join(products_folder, "weblog"))

os.system("cp pipeline_shelf.restore {}".format(products_folder))

# Make zipped tar files of the other 2 first

flags_folder = glob("*.ms.flagversions")
if len(flags_folder) == 0:
    raise ValueError("Found no flagversions folder")
if len(flags_folder) > 1:
    raise ValueError("Found multiple flagversions folders.")

flags_folder = flags_folder[0]
flags_tarfile = "{}.tgz".format(flags_folder)

if os.path.exists(flags_tarfile):
    os.system("rm -rf {}".format(flags_tarfile))

with tarfile.open(flags_tarfile, "w:gz") as tar:
    tar.add(flags_folder,
            arcname=os.path.basename(flags_folder))

os.system("mv {0} {1}".format(flags_tarfile, products_folder))

cals_folder = "final_caltables"
cals_tarfile = "caltables.tgz"

if os.path.exists(cals_tarfile):
    os.system("rm -rf {}".format(cals_tarfile))


with tarfile.open(cals_tarfile, "w:gz") as tar:
    tar.add(cals_folder,
            arcname=os.path.basename(cals_folder))

os.system("mv {0} {1}".format(cals_tarfile, products_folder))

# Now copy the products folder to the given backup location
# Use the parent directory name as the name for the backup file

parentdir = os.getcwd().split("/")[-1]

copy_tree(products_folder,
          os.path.join(backup_location, parentdir))
