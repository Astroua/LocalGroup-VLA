
# Look for a custom flagging script in the repo

import os
from shutil import copyfile

# Look for a custom flagging script in the repo and copy over.
parentdir = os.getcwd().split("/")[-1]

flag_filename = "{}_lines_flags.txt".format(parentdir)
flag_path = os.path.expanduser("~/LocalGroup-VLA/12A-304/track_flagging")
full_flag_filename = os.path.join(flag_path, flag_filename)

logprint("Looking for custom flag script", logfileout='logs/custom_flagging.log')


if os.path.exists(full_flag_filename):
    copyfile(full_flag_filename,
             "additional_flagging.txt")
    logprint("Found additional flagging script.", logfileout='logs/custom_flagging.log')

    # Now run flagdata and flagmanager

    default('flagdata')

    flagdata(vis=ms_active, inpfile='additional_flagging.txt',
    		 flagbackup=False, mode='list', action='apply')

    default('flagmanager')
    flagmanager(vis=ms_active, versionname='custom_flagging')
    logprint("Created custom flagging version.", logfileout='logs/custom_flagging.log')

else:
    print("No additional flagging script found in the LocalGroup-VLA repo"
          " for lines.")
    logprint("No additional flagging script found in the LocalGroup-VLA repo", logfileout='logs/custom_flagging.log')
