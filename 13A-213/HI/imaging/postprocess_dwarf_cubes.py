
'''
Run the postprocessing on the image cubes:
(1) Estimate noise levels
(2) Reproject the single dish data
(3) Run feathering statistics
(4) Run feathering
(5) Convert to K
(6) Run masking on VLA and VLA+SD cubes
'''

from spectral_cube import SpectralCube
import numpy as np
import astropy.units as u
from astropy.stats import mad_std
import matplotlib.pyplot as plt
import os
import scipy.ndimage as nd
from astropy import log
from glob import glob

from uvcombine.scale_factor import find_scale_factor

from cube_analysis.feather_cubes import feather_compare_cube
from cube_analysis.reprojection import reproject_cube


def taper_weights(mask, sigma, nsig_cut=3):

    dist = nd.distance_transform_edt(mask)

    gauss_dists = np.where(np.logical_and(dist < nsig_cut * sigma, dist > 0.))
    flat_dists = np.where(dist >= nsig_cut * sigma)

    weight_arr = np.zeros_like(mask, dtype=float)

    weight_arr[gauss_dists] = \
        np.exp(- (dist[gauss_dists] - nsig_cut * sigma)**2 / (2 * sigma**2))
    weight_arr[flat_dists] = 1.

    return weight_arr


gals = ['IC1613', 'SextansA', 'WLM']

sd_data = {"IC1613": "/home/ekoch/bigdata/ekoch/IC1613/EBHIS/SIN_A01.fits",
           'SextansA': "/home/ekoch/bigdata/ekoch/SextansA/EBHIS/SIN_A08.fit",
           "WLM": "/home/ekoch/bigdata/ekoch/WLM/HI4PI/SIN_D01.fits"}

vla_directories = {'IC1613': "/home/ekoch/bigdata/ekoch/IC1613/VLA/13A-213/HI/",
                   'SextansA': "/home/ekoch/bigdata/ekoch/SextansA/VLA/13A-213/HI/",
                   'WLM': "/home/ekoch/bigdata/ekoch/WLM/VLA/13A-213/HI/"}

noise_dict = {}
sc_factor_dict = {}

num_cores = 1

pblim = 0.2
pblim_feathcompare = 0.5
hi_freq = 1.42040575177 * u.GHz

# All of these tracks are C or D and have the same
# shortest baseline of ~35 m.
# Use something just a bit larger.
min_baseline = 40 * u.m

las = (hi_freq.to(u.cm, u.spectral()) / (40 * u.m))
las = las.to(u.arcsec, u.dimensionless_angles())

# Only use channels with signal in them for the UV-overlap
# comparison.
# We'll limit this to places where there is a strong peak
# detection
chan_minsig_thresh = 10.
# Use the first and last channels. Definitely safe here
# or likely any JVLA HI SPWs.
start_chan = 10
end_chan = 10


# Loop through galaxies
for gal in gals:

    # Loop through VLA directories
    # Skip those with no continuum subtraction

    imaging_dirs = glob(f"{vla_directories[gal]}/full_imaging*")

    for img_dir in imaging_dirs:
        if "wcont" in img_dir:
            continue

        img_dir_tag = f"{gal}_{img_dir.split('/')[-1]}"

        log.info(f"Running on cube from: {img_dir}")

        cube_name = glob(os.path.join(img_dir, "*image.pbcor.fits"))
        assert len(cube_name) == 1
        cube_name = cube_name[0]
        log.info(f"Found cube name: {cube_name}")

        pb_name = glob(os.path.join(img_dir, "*pb.fits"))
        assert len(pb_name) == 1
        pb_name = pb_name[0]
        log.info(f"Found pb name: {pb_name}")

        # (1) Grab, reproject, and save the SD data

        sd_cube_name = sd_data[gal]
        log.info(f"Using SD cube {sd_cube_name}")

        vla_cube = SpectralCube.read(cube_name)

        pb_cube = SpectralCube.read(pb_name)

        # Estimate the noise level
        start_samps = vla_cube[:start_chan].filled_data[:].value * \
            pb_cube[:start_chan].filled_data[:].value
        start_samps = start_samps[np.isfinite(start_samps)]
        end_samps = vla_cube[-end_chan:].filled_data[:].value * \
            pb_cube[-end_chan:].filled_data[:].value
        end_samps = end_samps[np.isfinite(end_samps)]

        samps = np.append(start_samps, end_samps)
        del start_samps
        del end_samps

        noise_val = mad_std(samps)
        del samps

        print(f"Noise level is: {noise_val} Jy/beam")

        noise_dict[img_dir_tag] = noise_val

        # Get the range of channels we should use for the overlap
        # comparison.
        mask_chans = np.zeros((vla_cube.shape[0]), dtype=bool)
        for chan in range(vla_cube.shape[0]):

            flatnoise_chan = vla_cube.filled_data[chan].value * pb_cube[chan].value

            if np.nanmax(flatnoise_chan) > chan_minsig_thresh * noise_val:
                mask_chans[chan] = True

        # Check for the interpolated version.
        sd_cube_name_base = sd_cube_name.rstrip(".fits")
        sd_cube_jybm_name = f"{sd_cube_name_base}_{img_dir_tag}_Jybm.fits"
        sd_cube_reproj_name = f"{sd_cube_name_base}_{img_dir_tag}_fullreproj_Jybm.fits"

        if not os.path.exists(sd_cube_reproj_name):

            sd_cube = SpectralCube.read(sd_cube_name)
            sd_cube.allow_huge_operations = True

            # Convert to Jy/beam.
            sd_cube = sd_cube.to(u.Jy / u.beam,
                                 sd_cube.beam.jtok_equiv(hi_freq))

            sd_cube.write(sd_cube_jybm_name, overwrite=True)

            del sd_cube

            # Save some memory...

            reproject_cube(sd_cube_jybm_name, cube_name,
                           sd_cube_reproj_name,
                           reproject_type='all',
                           chunk=30,
                           wcs_check=False)

            # Reproject to same spatial grid, too.
            # sd_cube = sd_cube.reproject(vla_cube.header)

            # Apply the same PB cut-off used in the VLA data.
            # spat_mask = np.isfinite(pb_cube[0])
            # sd_cube = sd_cube.with_mask(spat_mask)

            # Write out final matched version.
            # sd_cube.write(sd_cube_reproj_name, overwrite=True)

        sd_cube = SpectralCube.read(sd_cube_reproj_name)

        # Smoothly taper along the pblim threshold
        # This is set really high on purpose, where the VLA data
        # is closest to the pointing centre

        # Run feathering tests.

        weight = taper_weights(pb_cube[0] > pblim_feathcompare,
                               20, nsig_cut=5)

        radii, ratios, high_pts, low_pts, chan_out = \
            feather_compare_cube(vla_cube, sd_cube, las,
                                 num_cores=num_cores,
                                 chunk=100,
                                 verbose=False,
                                 weights=weight,
                                 relax_spectral_check=False,
                                 spec_check_kwargs={'rtol': 0.03})

        sc_factor, sc_err = find_scale_factor(np.hstack(low_pts[mask_chans]),
                                              np.hstack(high_pts[mask_chans]),
                                              method='distrib',
                                              verbose=True)

        scale_factor_figure = f"{img_dir}/{img_dir_tag}_scalefact"
        plt.grid(True)
        plt.xlabel(r"ln I$_{\rm int}$ / I$_{\rm SD}$")
        plt.xlim([-2, 2])
        plt.tight_layout()

        plt.savefig(f"{scale_factor_figure}.png")
        plt.savefig(f"{scale_factor_figure}.pdf")
        plt.close()

        print(f"SC factor for {sc_factor}+/-{sc_err}")

        # Just record all of the feathering cases to compare
        # and make sure things are working.
        sc_factor_dict[img_dir_tag] = [sc_factor, sc_err]

        continue

        if sc_factor < 0.9 or sc_factor > 1.1:
            sc_factor_use = float(input(f"Check scale factor and input value to use:"))
        else:
            sc_factor_use = sc_factor

        del vla_cube
        del pb_cube
        del sd_cube
        del low_pts
        del high_pts

    # Run feathering

    # Run masking and moment pipeline
    # Enable converting to K
