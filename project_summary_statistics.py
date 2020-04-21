
'''
Functions to return useful statistics from projects.

* Data flagged fraction after pipeline runs
* Cube noise vs. thermal noise

'''

import os
from glob import glob
import tarfile
import numpy as np
from pandas import DataFrame


def project_flagstats(path, per_spw=False,
                      spw_nums=np.arange(12).astype(int),
                      pipe_stage=14):
    '''
    Calculate the flagged fraction of the data for the tracks
    in a project.
    `path` should point to the location of the restore products,
    where each track has its own folder in `path`.
    The function then searches for the given stage in the weblog
    produced by the VLA pipeline and reads in the flagging statistics
    from the log file.
    '''

    folders = [fold for fold in glob(f"{path}/*") if os.path.isdir(fold)]

    flag_dict = {'Total': []}

    if per_spw:
        for spw in spw_nums:
            flag_dict[f"SPW_{spw}"] = []

    track_names = []

    for fold in folders:

        trackname = fold.split("/")[-1]

        track_names.append(trackname)

        has_weblog = os.path.exists(f"{fold}/weblog")
        pipe_folder = glob(f"{fold}/pipe*")
        has_pipeline = len(pipe_folder) == 1

        if has_weblog:
            pipe_folder = f"{fold}/weblog"

        # elif not has_pipeline or not has_weblog:
        else:
            # Unzip the weblog.
            weblog_tgz = f"{fold}/weblog.tgz"
            assert os.path.exists(weblog_tgz)
            with tarfile.open(weblog_tgz, "r:gz") as tar:
                tar.extractall(path=fold)
                tar.close()

            # Find the resulting pipe folder.
            pipe_folder = glob(f"{fold}/pipeline-*")
            if len(pipe_folder) == 1:
                pipe_folder = pipe_folder[0]
            else:
                # Just called weblog?
                pipe_folder = glob(f"{fold}/weblog")
                if not len(pipe_folder) == 1:
                    raise ValueError(f"Cannot find weblog folder for {trackname}")
                else:
                    pipe_folder = pipe_folder[0]

        # Find the log file.

        finalflag_log = f"{pipe_folder}/html/stage{pipe_stage}/casapy.log"

        if not os.path.exists(finalflag_log):
            raise ValueError("Cannot find final flag log {finalflag_log}")

        # Now we need to search through the log file for numbers.

        # There are multiple summary outputs. For now, just want
        # the total flagged fraction.
        flagout_str = "Summary::getResult"

        # Total fraction:
        match_str = "Total Flagged"
        with open(finalflag_log, 'rt') as logfile:

            lines = []

            for line in logfile:
                if line.find(match_str) > 0 and line.find(flagout_str) > 0:
                    lines.append(line)

            # Flag summary is run before and after applycal.
            # Want fraction after applycal
            thisline = lines[-1]

            # Get percent
            perc_flagged = float(thisline.split("(")[-1].split("%)")[0])

            # make fraction
            perc_flagged /= 100.

            flag_dict['Total'].append(perc_flagged)

        # Optionally do per SPW, too
        if per_spw:
            for spw in spw_nums:

                match_str = f"spw {int(spw)} flagged:"
                with open(finalflag_log, 'rt') as logfile:

                    lines = []

                    for line in logfile:
                        if line.find(match_str) > 0 and line.find(flagout_str) > 0:
                            lines.append(line)

                    # This SPW might not exist.
                    if len(lines) == 0:
                        flag_dict[f'SPW_{spw}'].append(np.NaN)
                        continue

                    # Flag summary is run before and after applycal.
                    # Want fraction after applycal
                    thisline = lines[-1]

                    # Get percent
                    perc_flagged = float(thisline.split("(")[-1].split("%)")[0])

                    # make fraction
                    perc_flagged /= 100.

                    flag_dict[f'SPW_{spw}'].append(perc_flagged)

        # Remove the expanded pipeline folder
        out = os.system(f"rm -r {pipe_folder}")
        assert out == 0

    # Output a table
    tab = DataFrame(flag_dict, index=track_names)

    return tab


def save_flagfrac_pilots(path, spw_type='Lines',
                         skip=['11B-124', '12A-304', '14B-088']):
    '''
    Save flagging fraction tables for all pilot projects.
    '''

    for proj in os.listdir(path):

        print(f"On {proj}")

        if not os.path.isdir(f"{path}/{proj}"):
            continue

        if proj in skip:
            continue

        backup_folder = f"{path}/{proj}/{spw_type}/"
        if not os.path.exists(backup_folder):
            print("Given directory {backup_folder} does not exist")
            continue


        # print(os.listdir(backup_folder))

        df = project_flagstats(backup_folder,
                               per_spw=True)

        basename = proj.split("/")[-1]
        # Save the dataframe out
        df.to_csv(f"{path}/{proj}/{basename}_{spw_type.lower()}_flagfractions.csv")

        # except Exception as exp:
        #     print(f"Failed for {proj} due to")
        #     print(exp)
