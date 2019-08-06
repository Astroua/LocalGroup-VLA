
'''
Image the C config tracks (i.e., all usable ones) for IC1613

To be run in CASA >5.5
'''

import os
import sys
import numpy as np

execfile(os.path.expanduser("~/ownCloud/code_development/LocalGroup-VLA/13A-213/spw_setup.py"))


use_contsub = True if sys.argv[-2] == 'True' else False

# Number of channels to use for each channel in the output cube
chan_width = int(sys.argv[-1])
spw_num = 0


gal_name = 'IC1613'

if use_contsub:
    myvis = 'IC1613_13A-213_HI_spw_0_LSRK.ms.contsub'
    output_path = "{0}_HI_imaging_chanwidth_{1}chan".format(gal_name, chan_width)
    imgname = '{0}_13A-213_{1}_spw_{2}.clean'.format(gal_name, "HI", spw_num)
else:
    myvis = 'IC1613_13A-213_HI_spw_0_LSRK.ms'
    output_path = "{0}_HI_imaging_wcont_chanwidth_{1}chan".format(gal_name, chan_width)
    imgname = '{0}_13A-213_{1}_spw_{2}_wcont.clean'\
        .format(gal_name, "HI", spw_num)

if not os.path.exists(output_path):
    os.mkdir(output_path)

mycellsize = '3arcsec'
casalog.post("Cell size: {}".format(mycellsize))

# Choose something low as there is some HI near the edges of the mosaic
mypblimit = 0.15

# Scale from the threshold value for one channel in these data
threshold_val_stage1 = 3.2  # mJy/bm
use_thresh = "{}mJy/beam".format(threshold_val_stage1 / np.sqrt(chan_width))
threshold_val_stage2 = 3.2  # mJy/bm
use_thresh2 = "{}mJy/beam".format(threshold_val_stage2 / np.sqrt(chan_width))

# Set to something fairly large.
myimagesize = 1200
casalog.post("Image size: {}".format(myimagesize))

# Calculate number of channels based on the width
# Round up for fractions
nchans = int(np.ceil(galaxy_dict[gal_name.lower()]['HI_nchan'] / chan_width))

casalog.post("Number of channels: {}".format(nchans))

default('tclean')

# Aggressive auto-masking w/ many major cycles to slowly
# grow the mask
tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
       spw=str(spw_num),
       field='{}*'.format(gal_name),
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=galaxy_dict[gal_name.lower()]['HI_start'],
       width=chan_width,
       nchan=nchans,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=200000,
       threshold=use_thresh,
       phasecenter=galaxy_dict[gal_name.lower()]['phasecenter'],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       deconvolver='multiscale',
       scales=[0, 4, 8, 20, 40, 80],
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=500,  # Force a lot of major cycles
       usemask='auto-multithresh',
       mask=None,
       pbmask=mypblimit,
       sidelobethreshold=2.5,
       noisethreshold=3.5,
       lownoisethreshold=2.0,
       negativethreshold=0.0,
       smoothfactor=3.0,
       minbeamfrac=0.8,
       cutthreshold=0.01,
       growiterations=75,
       fastnoise=False,
       verbose=True,
       )

# Backup from first stage
for suff in ['image', 'residual', 'mask']:
    inp_name = "{0}.{1}".format(imgname, suff)
    out_name = "{0}.{1}.stage1".format(imgname, suff)
    os.system("cp -r {0} {1}".format(os.path.join(output_path, inp_name),
                                     os.path.join(output_path, out_name)))

# Remove the mask
mask_name = "{0}.{1}".format(imgname, 'mask')
os.system("rm -r {}".format(os.path.join(output_path, mask_name)))

# We also have to delete these products from the workdir
workdir = "{0}.{1}".format(imgname, 'workdirectory')

# Remove workdir images
os.system("rm -rf {0}/*.image".format(os.path.join(output_path, workdir)))
# Remove workdir masks
os.system("rm -rf {0}/*.mask".format(os.path.join(output_path, workdir)))


# Low level emission not included in the mask.
# Pb-only mask
# Avoid clean diverging by forcing tons of major cycles (cycleniter=500)
# Ensures that bowls are not cleaned.
tclean(vis=myvis,
       datacolumn='corrected',
       imagename=os.path.join(output_path, imgname),
       spw=str(spw_num),
       field='{}*'.format(gal_name),
       imsize=myimagesize,
       cell=mycellsize,
       specmode='cube',
       start=galaxy_dict[gal_name.lower()]['HI_start'],
       width=chan_width,
       nchan=nchans,
       startmodel=None,
       gridder='mosaic',
       weighting='natural',
       niter=200000,
       threshold=use_thresh2,
       phasecenter=galaxy_dict[gal_name.lower()]['phasecenter'],
       restfreq="1.420405752GHz",
       outframe='LSRK',
       pblimit=mypblimit,
       deconvolver='multiscale',
       scales=[0, 4, 8, 20, 40, 80],
       pbcor=False,
       veltype='radio',
       chanchunks=-1,
       restoration=True,
       parallel=True,
       cycleniter=500,  # Force a lot of major cycles
       usemask='pb',
       mask=None,
       pbmask=mypblimit,
       calcres=False,
       calcpsf=False,
       )


# Apply pbcor on final version

impbcor(imagename='{}.image'.format(os.path.join(output_path, imgname)),
        pbimage='{}.pb'.format(os.path.join(output_path, imgname)),
        outfile='{}.image.pbcor'.format(os.path.join(output_path, imgname)))

# Into FITS

for suff in ['image.pbcor', 'image', 'pb', 'residual', 'psf']:

    exportfits(imagename='{0}.{1}'.format(os.path.join(output_path, imgname), suff),
               fitsimage='{0}.{1}.fits'.format(os.path.join(output_path, imgname), suff),
               velocity=True, optical=False,
               dropdeg=True, history=False)