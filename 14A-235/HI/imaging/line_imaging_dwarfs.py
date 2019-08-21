
'''
Should be run from the 14A-235 folder on cedar or SegFault

Meant for imaging NGC 185 and 205. The M31 cube is much much
larger with more complex emission.

Stage 1 cleaning - make a dirty cube. Calc PSF.

Stage 2 cleaning - clean to 2-sigma WITH auto-masking

Stage 3 cleaning - clean to 2-sigma without a clean mask.

To be run in CASA 5.5

'''

import os
import sys
import socket
import numpy as np
from spectral_cube import SpectralCube
from astropy.stats import mad_std

# Requires analysisutils to be appended to the casa path
# Load in the auto image parameter setters
# from CASA_functions import set_cellsize, set_imagesize

from tasks import tclean, listobs

# Load in the info dicts from the repo
host_name = socket.gethostname()
if host_name == 'segfault' or host_name == 'ewk':
    execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/14A-235/spw_setup.py"))
elif 'cedar' in host_name:
    execfile(os.path.expanduser("~/code/LocalGroup-VLA/14A-235/spw_setup.py"))
else:
    raise ValueError("Not running on SegFault or cedar? Unsure where the code repo is.")

# galaxy name given. And is folder name
gal_name = sys.argv[-5]

assert gal_name in fourteenA_sources.keys()

if gal_name == "M31":
    raise NotImplementedError("Do no use this script to image M31!")

use_contsub = True if sys.argv[-4] == 'True' else False

# Number of channels to use for each channel in the output cube
chan_width = int(sys.argv[-3])
spw_num = 0

# Weighting
use_weighting = sys.argv[-2]
if use_weighting not in ['natural', 'briggs', 'uniform']:
    raise ValueError("use_weighting not valid")

# Do in 2 stages. Second tclean can fail b/c some image files are not
# properly closed
stage = int(sys.argv[-1])

if stage < 1 or stage > 3:
    raise ValueError("stage must be 1, 2, or 3.")

if use_contsub:
    myvis = '{}_14A-235_HI_spw_0_LSRK.ms.contsub'.format(gal_name)
    output_path = "{0}_HI_imaging_chanwidth_{1}".format(gal_name, chan_width)
    if use_weighting == 'natural':
        imgname = '{0}_14A-235_{1}_spw_{2}_natural.clean'\
            .format(gal_name, "HI", spw_num)
    elif use_weighting == 'briggs':
        imgname = '{0}_14A-235_{1}_spw_{2}_robust0.clean'\
            .format(gal_name, "HI", spw_num)
        output_path += "_robust0"
    else:
        # uniform
        imgname = '{0}_14A-235_{1}_spw_{2}_uniform.clean'\
            .format(gal_name, "HI", spw_num)
        output_path += "_uniform"

    my_minbeamfrac = 0.8

else:
    myvis = '{}_14A-235_HI_spw_0_LSRK.ms'.format(gal_name)
    output_path = "{0}_HI_imaging_wcont_chanwidth_{1}".format(gal_name, chan_width)
    if use_weighting == 'natural':
        imgname = '{0}_14A-235_{1}_spw_{2}_wcont_natural.clean'\
            .format(gal_name, "HI", spw_num)
    elif use_weighting == 'briggs':
        imgname = '{0}_14A-235_{1}_spw_{2}_wcont_robust0.clean'\
            .format(gal_name, "HI", spw_num)
        output_path += "_robust0"
    else:
        # uniform
        imgname = '{0}_14A-235_{1}_spw_{2}_wcont_uniform.clean'\
            .format(gal_name, "HI", spw_num)
        output_path += "_uniform"

    my_minbeamfrac = 0.2

if not os.path.exists(output_path):
    os.mkdir(output_path)

# List the obs in the MS
listobs(myvis)

# Assume we can set reasonable image parameters from any of the tracks
if use_weighting == 'natural':
    mycellsize = '9arcsec'
elif use_weighting == 'briggs':
    mycellsize = '5arcsec'
else:
    mycellsize = '5arcsec'

# mycellsize = '9.3arcsec'
casalog.post("Cell size: {}".format(mycellsize))

# use robust=0 for Briggs weighting
use_robust = 0.

# Choose something low as there is some HI near the edges of the mosaic
mypblimit = 0.05
# mypblimit = 0.15

# Set to something fairly large.
if use_weighting == 'natural':
    myimagesize = 512
else:
    myimagesize = 1024

casalog.post("Image size: {}".format(myimagesize))

# Calculate number of channels based on the width
# Round up for fractions
nchans = int(np.ceil((fourteenA_HI_channels[gal_name]['end'] - fourteenA_HI_channels[gal_name]['start']) / chan_width))

casalog.post("Number of channels: {}".format(nchans))

# Image ALL channels in the MS. Just looking for reduction issues
default('tclean')

# Make a dirty cube

if stage == 1:
    tclean(vis=myvis,
           datacolumn='corrected',
           imagename=os.path.join(output_path, imgname),
           spw=str(spw_num),
           field='{}*'.format(gal_name),
           imsize=myimagesize,
           cell=mycellsize,
           specmode='cube',
           start=fourteenA_HI_channels[gal_name]['start'],
           width=chan_width,
           nchan=nchans,
           startmodel=None,
           gridder='mosaic',
           weighting=use_weighting,
           robust=use_robust,
           niter=0,
           threshold='',
           nsigma=5.,
           phasecenter=fourteenA_sources[gal_name],
           restfreq="1.420405752GHz",
           outframe='LSRK',
           pblimit=mypblimit,
           deconvolver='multiscale',
           scales=[0, 5, 10, 50],
           pbcor=False,
           veltype='radio',
           chanchunks=-1,
           restoration=False,
           parallel=False,
           cycleniter=1000,  # Force a lot of major cycles
           usemask='auto-multithresh',
           mask=None,
           pbmask=mypblimit,
           verbose=True,
           )

    # Copy the dirty residual into its own directory
    dirty_cube_path = os.path.join(output_path, "dirty_cube")

    if not os.path.exists(dirty_cube_path):
        os.mkdir(dirty_cube_path)

    dirty_residual_cube = os.path.join(output_path, imgname)
    os.system("cp -r {0}.residual {1}".format(dirty_residual_cube,
                                              dirty_cube_path))

    # Estimate noise from first few and last few channels
    cube = SpectralCube.read("{0}.residual".format(dirty_residual_cube),
                             format='casa_image')
    # First 5% and last 5%
    beg_cut = int(np.ceil(cube.shape[0] * 0.05))
    end_cut = int(np.floor(cube.shape[0] * 0.95))

    beg_noise = mad_std(cube.filled_data[:beg_cut][np.nonzero(cube[:beg_cut])])
    end_noise = mad_std(cube.filled_data[end_cut:][np.nonzero(cube[end_cut:])])

    casalog.post("Noise estimate from first 5 perc. of cube channels: {}"
                 .format(beg_noise))
    casalog.post("Noise estimate from last 5 perc. of cube channels: {}"
                 .format(end_noise))


# Scale from the threshold value for one channel in these data
if use_weighting == 'natural':
    threshold_val_stage1 = 7.  # mJy/bm
    use_thresh = "{}mJy/beam".format(threshold_val_stage1 / np.sqrt(chan_width))
    threshold_val_stage2 = 7.  # mJy/bm
    use_thresh2 = "{}mJy/beam".format(threshold_val_stage2 / np.sqrt(chan_width))
elif use_weighting == 'briggs':
    threshold_val_stage1 = 11.0  # mJy/bm
    use_thresh = "{}mJy/beam".format(threshold_val_stage1 / np.sqrt(chan_width))
    threshold_val_stage2 = 11.0  # mJy/bm
    use_thresh2 = "{}mJy/beam".format(threshold_val_stage2 / np.sqrt(chan_width))
else:  # uniform
    threshold_val_stage1 = 18.0  # mJy/bm
    use_thresh = "{}mJy/beam".format(threshold_val_stage1 / np.sqrt(chan_width))
    threshold_val_stage2 = 18.0  # mJy/bm
    use_thresh2 = "{}mJy/beam".format(threshold_val_stage2 / np.sqrt(chan_width))

if stage == 2:

    tclean(vis=myvis,
           datacolumn='corrected',
           imagename=os.path.join(output_path, imgname),
           spw=str(spw_num),
           field='{}*'.format(gal_name),
           imsize=myimagesize,
           cell=mycellsize,
           specmode='cube',
           start=fourteenA_HI_channels[gal_name]['start'],
           width=chan_width,
           nchan=nchans,
           startmodel=None,
           gridder='mosaic',
           weighting=use_weighting,
           robust=use_robust,
           niter=800000,
           threshold=use_thresh,
           # nsigma=5.,
           phasecenter=fourteenA_sources[gal_name],
           restfreq="1.420405752GHz",
           outframe='LSRK',
           pblimit=mypblimit,
           deconvolver='multiscale',
           scales=[0, 6, 12, 24, 80],
           pbcor=False,
           veltype='radio',
           chanchunks=-1,
           restoration=True,
           parallel=False,
           cycleniter=500,  # Force a lot of major cycles
           usemask='auto-multithresh',
           mask=None,
           pbmask=mypblimit,
           sidelobethreshold=2.5,
           noisethreshold=3.5,
           lownoisethreshold=2.0,
           negativethreshold=0.0,
           smoothfactor=3.0,
           minbeamfrac=my_minbeamfrac,
           cutthreshold=0.01,
           growiterations=75,
           fastnoise=False,
           verbose=True,
           calcres=False,
           calcpsf=False,
           )


if stage == 3:

    # Backup from first stage
    for suff in ['image', 'residual', 'mask']:
        inp_name = "{0}.{1}".format(imgname, suff)
        out_name = "{0}.{1}.stage1".format(imgname, suff)
        os.system("cp -r {0} {1}".format(os.path.join(output_path, inp_name),
                                         os.path.join(output_path, out_name)))

    # Remove the mask and image
    mask_name = "{0}.{1}".format(imgname, 'mask')
    os.system("rm -r {}".format(os.path.join(output_path, mask_name)))
    img_name = "{0}.{1}".format(imgname, 'image')
    os.system("rm -r {}".format(os.path.join(output_path, img_name)))

    # We also have to delete these products from the workdir when running
    # in parallel
    workdir = "{0}.{1}".format(imgname, 'workdirectory')

    # Remove workdir images
    os.system("rm -rf {0}/*.image".format(os.path.join(output_path, workdir)))
    # Remove workdir masks
    os.system("rm -rf {0}/*.mask".format(os.path.join(output_path, workdir)))


    tclean(vis=myvis,
           datacolumn='corrected',
           imagename=os.path.join(output_path, imgname),
           spw=str(spw_num),
           field='{}*'.format(gal_name),
           imsize=myimagesize,
           cell=mycellsize,
           specmode='cube',
           start=fourteenA_HI_channels[gal_name]['start'],
           width=chan_width,
           nchan=nchans,
           startmodel=None,
           gridder='mosaic',
           weighting=use_weighting,
           robust=use_robust,
           niter=1000000,
           threshold=use_thresh2,
           phasecenter=fourteenA_sources[gal_name],
           restfreq="1.420405752GHz",
           outframe='LSRK',
           pblimit=mypblimit,
           deconvolver='multiscale',
           scales=[0, 6, 12, 24, 80],
           pbcor=False,
           veltype='radio',
           chanchunks=-1,
           restoration=True,
           parallel=False,
           cycleniter=500,
           usemask='pb',
           mask=None,
           pbmask=mypblimit,
           verbose=True,
           calcres=False,
           calcpsf=False,
           )

    # Apply pbcor on final version

    impbcor(imagename='{}.image'.format(os.path.join(output_path, imgname)),
            pbimage='{}.pb'.format(os.path.join(output_path, imgname)),
            outfile='{}.image.pbcor'.format(os.path.join(output_path, imgname)),
            overwrite=True)

    # Into FITS

    for suff in ['image.pbcor', 'image', 'pb', 'residual', 'psf']:

        exportfits(imagename='{0}.{1}'.format(os.path.join(output_path, imgname), suff),
                   fitsimage='{0}.{1}.fits'.format(os.path.join(output_path, imgname), suff),
                   velocity=True, optical=False,
                   dropdeg=True, history=False, overwrite=True)
