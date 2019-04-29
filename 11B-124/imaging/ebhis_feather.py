
'''
Feather with the EBHIS data.
'''

from spectral_cube import SpectralCube
import os
from os.path import join as osjoin
from astropy import log
import scipy.ndimage as nd
import numpy as np
import astropy.units as u

from cube_analysis.feather_cubes import feather_cube
from cube_analysis.reprojection import reproject_cube
from cube_analysis.register_cubes import (cube_registration,
                                          spatial_shift_cube)

# from paths import (seventeenB_HI_data_02kms_path,
#                    seventeenB_HI_data_1kms_path,
#                    data_path)
# from constants import hi_freq


hi_freq = 1.42040575177 * u.GHz


do_prep_ebhis = True
do_feather = False

num_cores = 4
chunk = 8

# 11B cube
elevenB_folder = os.path.expanduser("~/space/ekoch/VLA_tracks/11B-124/")
elevenB_name = "M31_11B-124_HI_spw_0.clean.image.pbcor.fits"


if do_prep_ebhis:

    ebhis_folder = os.path.expanduser("~/bigdata/ekoch/M31/EBHIS/")

    ebhis_name = "CAR_C01.fits"

    out_name = "CAR_C01_11B124_match.fits"

    reproject_cube(osjoin(ebhis_folder, ebhis_name),
                   osjoin(elevenB_folder, elevenB_name),
                   out_name,
                   output_folder=ebhis_folder,
                   save_spectral=False,
                   is_huge=True,
                   reproject_type='all',
                   common_beam=False,  # Already common beam
                   verbose=True,
                   chunk=100,
                   wcs_check=False)
    # Remove wcs check. It fails for a reason that is currently unclear to me
    # The WCS info looks the same...

    # Register the cubes next.
    cube = SpectralCube.read(osjoin(ebhis_folder, out_name))
    elevenB_cube = SpectralCube.read(osjoin(elevenB_folder, elevenB_name))

    offsets = cube_registration(cube, elevenB_cube,
                                verbose=True,
                                num_cores=1,
                                restfreq=hi_freq)

    mean_offsets = np.mean(offsets, axis=0)

    input("Offsets are {}. Accept?".format(mean_offsets))

    dy, dx = mean_offsets

    out_name = "CAR_C01_11B124_match.spatregistered.fits"

    spatial_shift_cube(cube, dy, dx,
                       verbose=True, save_shifted=True,
                       save_name=osjoin(ebhis_folder, out_name),
                       num_cores=num_cores, chunk=100)


if do_feather:

    def taper_weights(mask, sigma, nsig_cut=3):
        '''
        This needs to be moved to uvcombine.
        '''

        dist = nd.distance_transform_edt(mask)

        gauss_dists = np.where(np.logical_and(dist < nsig_cut * sigma, dist > 0.))
        flat_dists = np.where(dist >= nsig_cut * sigma)

        weight_arr = np.zeros_like(mask, dtype=float)

        weight_arr[gauss_dists] = \
            np.exp(- (dist[gauss_dists] - nsig_cut * sigma)**2 / (2 * sigma**2))
        weight_arr[flat_dists] = 1.

        return weight_arr


    # Load the non-pb masked cube
    elevenB_cube = SpectralCube.read(osjoin(elevenB_folder, elevenB_name))

    elevenB_pb_name = "M31_11B-124_HI_spw_0.clean.pb.fits"
    pb_cube = SpectralCube.read(osjoin(elevenB_folder, elevenB_pb_name))
    # PB minimally changes over the frequency range. So just grab one plane
    pb_plane = pb_cube[0]

    # Smoothly taper data at the mosaic edge. This weight array tapers to
    # exp(-5^2/2)~4e-6 at the pb cut-off of 0.2.
    weight = taper_weights(np.isfinite(pb_plane), 30, nsig_cut=5)

    ebhis_folder = os.path.expanduser("~/bigdata/ekoch/M31/EBHIS/")
    out_name = "CAR_C01_11B124_match.fits"
    cube = SpectralCube.read(osjoin(ebhis_folder, out_name))

    save_name = osjoin(elevenB_folder,
                       "M31_11B-124_HI_spw_0.clean.pbcor.EBHIS_feather.fits")

    feather_cube(elevenB_cube, cube, restfreq=hi_freq, save_feather=True,
                 save_name=save_name, num_cores=1,
                 weights=weight, chunk=chunk, verbose=True)
