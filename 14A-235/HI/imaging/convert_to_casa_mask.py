'''
Use the output of mask_cleanmask.py and convert into a CASA image.
'''

import os
import numpy as np

from tasks import importfits

from paths import ebhis_m31_HI_data_path


osjoin = os.path.join

ebhis_outpath = ebhis_m31_HI_data_path('14A-235_items', no_check=True)

run_04kms = True

if run_04kms:

    save_name = "CAR_C01_14A235_match_04kms_1K_mask.fits"
    out_name = "CAR_C01_14A235_match_04kms_1K_mask.image"

    mask_save_name = osjoin(ebhis_outpath, save_name)
    mask_out_name = osjoin(ebhis_outpath, out_name)

    # Adding the deg axis is not working in some cases?
    importfits(fitsimage=mask_save_name, imagename=mask_out_name,)
               # defaultaxes=True,
               # defaultaxesvalues=["", "", "", "I"])

    ia.open(mask_out_name)
    ia.adddegaxes(outfile=mask_out_name + ".stokes", stokes='I')
    ia.close()

    # Split off each channel
    out_path = osjoin(ebhis_outpath, "mask_1kms_chans/")

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    # Open image.
    ia.open(mask_out_name + ".stokes")

    # Find the spectral axis
    csys = ia.coordsys()

    # Check this name??
    specaxis_name = "Frequency"
    spec_axis = np.where(np.asarray(csys.names()) == specaxis_name)[0][0]

    cube_shape = list(ia.shape())
    ndims = len(cube_shape)
    nchan = cube_shape[spec_axis]

    lower_corner = [0] * ndims
    upper_corner = cube_shape

    for chan in range(nchan):

        casalog.post("Channel {}".format(chan))

        # Set the channel
        lower_corner[spec_axis] = chan
        upper_corner[spec_axis] = chan

        box = rg.box(lower_corner, upper_corner)

        # Now make sliced image
        chan_name = "{0}_channel_{1}".format(mask_out_name.split("/")[-1], chan)
        im_slice = ia.subimage(os.path.join(out_path, chan_name),
                               box)
        im_slice.done()

    ia.close()
