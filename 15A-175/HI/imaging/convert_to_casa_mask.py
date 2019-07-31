'''
Use the output of mask_cleanmask.py and convert into a CASA image.
'''

import os
import numpy as np

from tasks import importfits

from taskinit import iatool
ia = iatool()

from paths import (fourteenA_HI_data_path,
                   ebhis_m31_HI_data_path,
                   fifteenA_HI_BC_1_2kms_data_path,
                   fifteenA_HI_BCtaper_04kms_data_path,
                   fourteenA_HI_file_dict,
                   m31_data_path)

run_12kms_BC = True
run_04kms_BC_taper = False


if run_12kms_BC:

    mask_save_name = fifteenA_HI_BC_1_2kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BC_1_2kms.fits",
                                            no_check=True)
    mask_out_name = fifteenA_HI_BC_1_2kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BC_1_2kms.image",
                                            no_check=True)


    # Adding the deg axis is not working in some cases?
    importfits(fitsimage=mask_save_name, imagename=mask_out_name,)
               # defaultaxes=True,
               # defaultaxesvalues=["", "", "", "I"])

    ia.open(mask_out_name)
    ia.adddegaxes(outfile=mask_out_name + ".stokes", stokes='I')
    ia.close()

    # Split off each channel
    out_path = os.path.join(fifteenA_HI_BC_1_2kms_data_path("", no_check=True), "mask_1_2kms_chans/")

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

if run_04kms_BC_taper:

    mask_save_name = fifteenA_HI_BCtaper_04kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BCtaper_0_4kms.fits",
                                            no_check=True)
    mask_out_name = fifteenA_HI_BCtaper_04kms_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor_source_mask_15A_BCtaper_0_4kms.image",
                                            no_check=True)


    # Adding the deg axis is not working in some cases?
    importfits(fitsimage=mask_save_name, imagename=mask_out_name,)
               # defaultaxes=True,
               # defaultaxesvalues=["", "", "", "I"])

    ia.open(mask_out_name)
    ia.adddegaxes(outfile=mask_out_name + ".stokes", stokes='I')
    ia.close()

    # Split off each channel
    out_path = os.path.join(fifteenA_HI_BCtaper_04kms_data_path("", no_check=True), "mask_04kms_chans/")

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
