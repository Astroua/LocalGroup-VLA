

import sys
import os
import re
import numpy as np
import time
import scipy.ndimage as nd
from glob import glob
import socket
import tarfile

from tasks import tclean, tget

'''
Stage 2 of cleaning single channels.

Expects that the data have been cleaned to 5-sigma with
HI_single_channel_clean.py

Stage 2 creates a clean mask based on the 5-sigma-cleaned image by identifying
the emission footprint. The cleaning is continued on the masked region to
~2-sigma.

It's likely best to limit the largest scales used for multi-scale clean here,
unlike the first stage.
'''

# Load in the SPW dict in the repo on cedar
if socket.gethostname().lower() == 'segfault':
    execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/15A-175/spw_setup.py"))
else:
    execfile(os.path.expanduser("~/code/LocalGroup-VLA/15A-175/spw_setup.py"))

chan_num = int(sys.argv[-3])

# Load in the imaging parameters from the given file name
parameter_file = sys.argv[-2]

# Assume file structure of channel_path/channel_${num}/
# Need to give the overall channel_path
channel_path = sys.argv[-1]

# Load parameters
tget(tclean, parameter_file)

# Append the full channel path to the vis's

vis = os.path.join(channel_path, "channel_{}".format(chan_num),
                   "{0}_chan_{1}".format(vis, chan_num))


# Now update the imagename with the channel number
imagename = os.path.join(channel_path, "channel_{}".format(chan_num),
                         "{0}_channel_{1}".format(imagename, chan_num))

# Based on the channel number, update the start velocity for this channel

# Get the value out from the string, removing the unit
try:
    split_start = filter(None, re.split(r'(\d+)', start))

    init_start = float("".join(split_start[:-1]))
    spec_unit = split_start[-1]

    chan_width = float("".join(filter(None, re.split(r'(\d+)', width))[:-1]))

    start_vel = init_start + chan_width * chan_num

    int_settings = False

except Exception:
    int_settings = True

# Check if the summary dictionary has already been saved for this channel
# If so, there is no need to clean any further

summ_files = glob("{}*.npy".format(imagename))

if len(summ_files) == 2:
    casalog.post("Summary file already exists! No need to clean further!")
    import sys
    sys.exit(0)

do_calcres = False
do_calcpsf = False

# Force startmodel to use the model on disk
startmodel = None

# Grab freq from the SPW dict
spw_num = 0

# Only update a few parameters, as needed

if not int_settings:
    start = "{0}{1}".format(start_vel, spec_unit)
    width = "{0}{1}".format(chan_width, spec_unit)
    nchan = 1
else:
    start = 1
    width = 1
    nchan = 1

restfreq = linespw_dict[spw_num][1]
restart = True
calcres = do_calcres
calcpsf = do_calcpsf
interactive = 0  # Returns a summary dictionary

# Untar the workdirectory folder
casalog.post("Making workdirectory tar file.")

workdir = "{}.workdirectory".format(imagename)
workdirtar = "{}.tar".format(workdir)

with tarfile.open(workdirtar, mode='r') as archive:
    archive.extractall()

os.system("rm -rf {}".format(workdirtar))

casalog.post("Finished making workdirectory tar file.")

# We're switching from auto-masking to pb masking for the final step
# ensuring that we get all emission above the limit.
# Need to delete the mask and image files from the workdir
os.system("rm -rf {}".format(os.path.join(workdir, "*.image")))
os.system("rm -rf {}".format(os.path.join(workdir, "*.mask")))

# Don't do this if we're using a signal mask from the 14B-only
# imaging.
# If the original mask still exists, remove it
old_maskname = "{0}.mask".format(imagename)
old_maskname_move = "{0}.mask.stage1".format(imagename)
os.system("cp -r {0} {1}".format(old_maskname, old_maskname_move))

if os.path.exists(old_maskname):
    os.system("rm -r {}".format(old_maskname))

# Make a copy of the stage 1 image
old_imagename = "{0}.image".format(imagename)
old_imagename_move = "{0}.image.stage1".format(imagename)
os.system("cp -r {0} {1}".format(old_imagename, old_imagename_move))

# Remove the original image file
os.system("rm -r {0}".format(old_imagename))

# And residual
old_residualname = "{0}.residual".format(imagename)
old_residualname_move = "{0}.residual.stage1".format(imagename)
os.system("cp -r {0} {1}".format(old_residualname, old_residualname_move))

# from imagerhelpers.imager_base import PySynthesisImager
from imagerhelpers.imager_parallel_continuum import PyParallelContSynthesisImager
from imagerhelpers.input_parameters import ImagerParameters

inpparams = locals().copy()
inpparams['msname'] = inpparams.pop('vis')
inpparams['timestr'] = inpparams.pop('timerange')
inpparams['uvdist'] = inpparams.pop('uvrange')
inpparams['obs'] = inpparams.pop('observation')
inpparams['state'] = inpparams.pop('intent')
inpparams['loopgain'] = inpparams.pop('gain')
inpparams['scalebias'] = inpparams.pop('smallscalebias')
defparm = dict(zip(ImagerParameters.__init__.__func__.__code__.co_varnames[1:],
                   ImagerParameters.__init__.func_defaults))
bparm = {k: inpparams[k] if k in inpparams else defparm[k] for k in defparm}
paramList = ImagerParameters(**bparm)

# imager = PySynthesisImager(params=paramList)
imager = PyParallelContSynthesisImager(params=paramList)

# Initialize modules major cycle modules
try:
    t0 = time.time()

    imager.initializeImagers()
    imager.initializeNormalizers()
    imager.setWeighting()

    t1 = time.time()

    casalog.post("Time for initializing imager and normalizers: " +
                 "%.2f" % (t1 - t0) + " sec")

    # Init minor cycle modules
    if restoration and niter > 0:
        t2 = time.time()
        imager.initializeDeconvolvers()
        t3 = time.time()
        casalog.post("Time for initializing deconvolver: " +
                     "%.2f" % (t3 - t2) + " sec")

    if niter > 0:
        t4 = time.time()
        imager.initializeIterationControl()
        t5 = time.time()
        casalog.post("Time for initializing iteration control: " +
                     "%.2f" % (t5 - t4) + " sec")

    # (5) Make the initial images

    if do_calcpsf:
        t6 = time.time()
        imager.makePSF()
        t7 = time.time()
        casalog.post("Time for creating PSF: " +
                     "%.2f" % (t7 - t6) + " sec")

        t8 = time.time()
        imager.makePB()
        t9 = time.time()
        casalog.post("Time for creating PB: " +
                     "%.2f" % (t9 - t8) + " sec")

    if do_calcres:
        casalog.post("Initial major cycle")

        t10 = time.time()
        imager.runMajorCycle()  # Make initial dirty / residual image
        t11 = time.time()
        casalog.post("Time for initial major cycle: " +
                     "%.2f" % (t11 - t10) + " sec")

        # Copy the initial residual map to a new name for post-imaging checks
        os.system("cp -r {0} {0}_init".format(imagename + ".residual"))

    if niter > 0:

        # (6) Make the initial clean mask
        imager.hasConverged()
        imager.updateMask()

        # (7) Run the iteration loops

        # Add an additional stopping criteria when the model flux between
        # major cycles changes by less than a set threshold.
        # Setting threshold to be 0.1%
        delta_model_flux_thresh = 1e-3

        model_flux_criterion = False

        mincyc_num = 0

        while not imager.hasConverged():
            # casalog.post("On minor cycle {}".format(mincyc_num))

            t0_l = time.time()
            imager.runMinorCycle()
            t1_l = time.time()
            casalog.post("Time for minor cycle: " +
                         "%.2f" % (t1_l - t0_l) + " sec")

            t2_l = time.time()
            imager.runMajorCycle()
            t3_l = time.time()
            casalog.post("Time for major cycle: " +
                         "%.2f" % (t3_l - t2_l) + " sec")

            summ = imager.IBtool.getiterationsummary()

            if mincyc_num == 0:
                model_flux_criterion = False
            else:
                model_flux_prev = summ['summaryminor'][2, :][-2]
                model_flux = summ['summaryminor'][2, :][-1]

                casalog.post("Previous model flux {0}. New model flux {1}".format(model_flux_prev, model_flux))

                model_flux_criterion = np.allclose(model_flux, model_flux_prev,
                                                   rtol=delta_model_flux_thresh)

            # Also require being close to the threshold, which we usually are
            # setting to 2-sigma
            # Require being below 2.5 sigma


            # Has the model converged?
            # if model_flux_criterion:
            #     casalog.post("Model flux converged to within {}% between "
            #                  "major cycles.".format(delta_model_flux_thresh * 100))
            #     break
            # else:
            #     time.sleep(10)

            imager.updateMask()

            time.sleep(10)

            mincyc_num += 1

    if niter > 0:
        out_dict = imager.IBtool.getiterationsummary()

        # Save the output dictionary. Numpy should be fine for this as the
        # individual channels will get concatenated together

        np.save(imagename + ".results_dict_stage2.npy", out_dict)

    if restoration:
        t12 = time.time()
        imager.restoreImages()
        t13 = time.time()
        casalog.post("Time for restoring images: " +
                     "%.2f" % (t13 - t12) + " sec")

        if pbcor:
            t14 = time.time()
            imager.pbcorImages()
            t15 = time.time()
            casalog.post("Time for pb-correcting images: " +
                         "%.2f" % (t15 - t14) + " sec")

    imager.deleteTools()

    t16 = time.time()
    casalog.post("Total Time: " +
                 "%.2f" % (t16 - t0) + " sec")


except Exception as e:
    casalog.post("Exception reported: {}".format(e), "SEVERE")
    casalog.post("Exception reported: {}".format(e.args), "SEVERE")

    try:
        imager.deleteTools()
    except Exception:
        pass

    raise e

# Convert the workdirectory to a tar file to create less files on scratch
casalog.post("Making workdirectory tar file.")

workdir = "{}.workdirectory".format(imagename)
workdirtar = "{}.tar".format(workdir)

with tarfile.open(workdirtar, mode='w') as archive:
    archive.add(workdir, recursive=True)

os.system("rm -rf {}".format(workdir))

casalog.post("Finished making workdirectory tar file.")
