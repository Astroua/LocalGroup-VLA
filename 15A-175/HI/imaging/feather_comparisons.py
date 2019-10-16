
'''
Compare the data where they overlap in the uv plane.

No offset correction is needed.
'''

from spectral_cube import SpectralCube
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
import os
import scipy.ndimage as nd

from uvcombine.scale_factor import find_scale_factor

from cube_analysis.feather_cubes import feather_compare_cube

from paths import (fifteenA_HI_BC_1_2kms_data_path,
                   fifteenA_HI_BCtaper_04kms_data_path,
                   ebhis_m31_HI_data_path,
                   allfigs_path)

from constants import hi_freq
from plotting_styles import onecolumn_figure

run_dict = dict(run_BCDtaper_04kms=False,
                run_BCD_1_2kms=True)

# We need to define a tapered weighting function to ignore emission outside
# of the VLA mosaic


def taper_weights(mask, sigma, nsig_cut=3):

    dist = nd.distance_transform_edt(mask)

    gauss_dists = np.where(np.logical_and(dist < nsig_cut * sigma, dist > 0.))
    flat_dists = np.where(dist >= nsig_cut * sigma)

    weight_arr = np.zeros_like(mask, dtype=float)

    weight_arr[gauss_dists] = \
        np.exp(- (dist[gauss_dists] - nsig_cut * sigma)**2 / (2 * sigma**2))
    weight_arr[flat_dists] = 1.

    return weight_arr


for key in run_dict:

    print(f"On {key}")

    if not run_dict[key]:
        print('Skipping.')
        continue

    # Change filenames and output plots with key name
    if key == 'run_BCDtaper_04kms':

        vla_cube = SpectralCube.read(fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.image.fits"))

        pb_cube = SpectralCube.read(fifteenA_HI_BCtaper_04kms_data_path("M31_15A_B_C_14A_HI_contsub_width_0_4kms.pb.fits"))

        ebhis_name = ebhis_m31_HI_data_path(
                          "15A-175_items/CAR_C01_15A175_match_04kms_spectralregrid.fits")
        ebhis_cube = SpectralCube.read(ebhis_name)

        # Update for each cube. Pick out channels where most of the emission
        # is captured for a robust estimate of the VLA/SD correction factor.
        chan_range = slice(200, 500)

    elif key == 'run_BCD_1_2kms':

        # TODO: update file names. Will safely fail here now.
        vla_cube = SpectralCube.read(fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.image.fits"))

        pb_cube = SpectralCube.read(fifteenA_HI_BC_1_2kms_data_path("M31_15A_B_C_14A_HI_contsub_width_1_2kms.pb.fits"))

        # weight = pb_cube[0].value

        ebhis_name = ebhis_m31_HI_data_path(
                          "15A-175_items/CAR_C01_15A175_match_12kms_spectralregrid.fits")
        ebhis_cube = SpectralCube.read(ebhis_name)

        chan_range = slice(50, 200)


    else:
        raise ValueError("")

    plot_label = key.lstrip('run_')

    pblim = 0.5
    # weight = taper_weights(np.isfinite(pb_cube[0]), 20, nsig_cut=5)
    weight = taper_weights(pb_cube[0] > pblim, 20, nsig_cut=5)

    # The shortest baseline for D-config is 35 m.
    # ms gives ~40 m so use that to be safe
    # All of these cubes contain C+D config so this is a safe assumption
    las = (hi_freq.to(u.cm, u.spectral()) / (40 * u.m))
    las = las.to(u.arcsec, u.dimensionless_angles())

    radii, ratios, high_pts, low_pts, chan_out = \
        feather_compare_cube(vla_cube, ebhis_cube, las,
                             num_cores=1,
                             chunk=250,
                             verbose=False,
                             weights=weight,
                             relax_spectral_check=False,
                             spec_check_kwargs={'rtol': 0.03})

    onecolumn_figure()
    sc_factor, sc_err = find_scale_factor(np.hstack(low_pts),
                                          np.hstack(high_pts),
                                          method='distrib',
                                          verbose=True)

    plt.grid(True)
    plt.xlabel(r"ln I$_{\rm int}$ / I$_{\rm SD}$")
    plt.xlim([-2, 2])
    plt.tight_layout()

    # Make sure the folder exists
    if not os.path.exists(allfigs_path("15A-175_imaging")):
        os.mkdir(allfigs_path("15A-175_imaging"))

    plt.savefig(allfigs_path("15A-175_imaging/ratio_hist_{plot_label}_vla_ebhis_w_weights.png"))
    plt.savefig(allfigs_path("15A-175_imaging/ratio_hist_{plot_label}_vla_ebhis_w_weights.pdf"))

    print("Factor: {0}+/-{1}".format(sc_factor, sc_err))
    # For 0.4 km/s tapered:
    # Factor: 0.619969810731763+/-0.0021213320488624064
    # For 1.2 km/s:
    # Factor: 0.5509672856367774+/-0.004333323268235445

    plt.close()

    # Compare properties per-channel
    sc_factor_chans = []
    sc_err_chans = []
    for low, high in zip(low_pts, high_pts):
        sc_f, sc_e = \
            find_scale_factor(low, high,
                              method='distrib',
                              verbose=False)
        sc_factor_chans.append(sc_f)
        sc_err_chans.append(sc_e)


    sc_factor_chans_linfit = []
    sc_err_chans_linfit = []
    for low, high in zip(low_pts, high_pts):
        sc_f, sc_e = \
            find_scale_factor(low, high,
                              method='linfit',
                              verbose=False)
        sc_factor_chans_linfit.append(sc_f)
        sc_err_chans_linfit.append(sc_e)

    sc_factor_chans_linfit = np.array(sc_factor_chans_linfit)
    sc_err_chans_linfit = np.array(sc_err_chans_linfit)

    chans = np.arange(len(low_pts))

    onecolumn_figure()
    plt.errorbar(chans, sc_factor_chans,
                 yerr=sc_err_chans,
                 alpha=0.5, label='Distrib Fit')
    plt.errorbar(chans, sc_factor_chans_linfit,
                 yerr=[sc_factor_chans_linfit - sc_err_chans_linfit[:, 0],
                       sc_err_chans_linfit[:, 1] - sc_factor_chans_linfit],
                 alpha=0.5, label='Linear fit')
    # plt.plot(chans, slope_lowess_85)
    plt.axhline(1, linestyle='--')
    plt.legend(frameon=True)
    plt.ylabel(r"Scale Factor")
    plt.xlabel("Channels")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(allfigs_path(f"15A-175_imaging/ratio_hist_perchan_{plot_label}_vla_ebhis_w_weights.png"))
    plt.savefig(allfigs_path(f"15A-175_imaging/ratio_hist_perchan_{plot_label}_vla_ebhis_w_weights.pdf"))
    plt.close()

    onecolumn_figure()
    sc_factor_chrange, sc_err_chrange = \
        find_scale_factor(np.hstack(low_pts[chan_range]),
                          np.hstack(high_pts[chan_range]),
                          method='distrib',
                          verbose=True)

    plt.grid(True)
    plt.xlabel(r"ln I$_{\rm int}$ / I$_{\rm SD}$")
    plt.tight_layout()
    plt.savefig(allfigs_path(f"15A-175_imaging/ratio_hist_{plot_label}_vla_ebhis_chan_{chan_range.start}_{chan_range.stop}_w_weights.png"))
    plt.savefig(allfigs_path(f"15A-175_imaging/ratio_hist_{plot_label}_vla_ebhis_chan_{chan_range.start}_{chan_range.stop}_w_weights.pdf"))

    print("Factor: {0}+/-{1}".format(sc_factor_chrange, sc_err_chrange))
    # For 0.4 km/s tapered:
    # Factor: Factor: 0.7365773477333422+/-0.002633281329603794

    # For 1.2 km/s:
    # Factor: 0.6794204263603334+/-0.005574160643158663
    # Error still underestimated

    # These are poor fits. Will need to look into with more detail.

    plt.close()
