
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

from paths import (fourteenA_HI_data_path,
                   ebhis_m31_HI_data_path,
                   m31_data_path,
                   allfigs_path)

from constants import hi_freq
from plotting_styles import onecolumn_figure


vla_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.image.fits"))

pb_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits"))

# weight = pb_cube[0].value

ebhis_name = ebhis_m31_HI_data_path(
                  "14A-235_items/CAR_C01_14A235_match_04kms_spectralregrid.fits")
ebhis_cube = SpectralCube.read(ebhis_name)

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


pblim = 0.5
# weight = taper_weights(np.isfinite(pb_cube[0]), 20, nsig_cut=5)
weight = taper_weights(pb_cube[0] > pblim, 20, nsig_cut=5)

# The shortest baseline for D-config is 35 m.
# ms gives ~40 m so use that to be safe
las = (hi_freq.to(u.cm, u.spectral()) / (40 * u.m)).to(u.arcsec, u.dimensionless_angles())

radii, ratios, high_pts, low_pts, chan_out = \
    feather_compare_cube(vla_cube, ebhis_cube, las,
                         num_cores=1,
                         chunk=250,
                         verbose=False,
                         weights=weight,
                         relax_spectral_check=False,
                         spec_check_kwargs={'rtol': 0.03})

onecolumn_figure()
sc_factor, sc_err = find_scale_factor(np.hstack(low_pts), np.hstack(high_pts),
                                      method='distrib',
                                      verbose=True)

plt.grid(True)
plt.xlabel(r"ln I$_{\rm int}$ / I$_{\rm SD}$")
plt.xlim([-2, 2])
plt.tight_layout()
plt.savefig(allfigs_path("14A-235_imaging/ratio_hist_14A_vla_ebhis_w_weights_v3.png"))
plt.savefig(allfigs_path("14A-235_imaging/ratio_hist_14A_vla_ebhis_w_weights_v3.pdf"))

print("Factor: {0}+/-{1}".format(sc_factor, sc_err))
# Factor: 1.115252652407311+/-0.00041563756216537193
# This is a bit higher than the factor below where the whole emission isn't
# quite captured in the VLA mosaic. Would need to re-run but this was ~1.17

# This isn't a fantastic fit, so this error was significantly underestimated

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

plt.savefig(allfigs_path("14A-235_imaging/ratio_hist_perchan_14A_ebhis_w_weights_v3.png"))
plt.savefig(allfigs_path("14A-235_imaging/ratio_hist_perchan_14A_ebhis_w_weights_v3.pdf"))
plt.close()

# Now refit with the channels near the systemic velocity, where most of the HI
# structure falls within the mosaic PB
# chan_range = slice(200, 1200)
chan_range = slice(500, 1000)

onecolumn_figure()
sc_factor_chrange, sc_err_chrange = \
    find_scale_factor(np.hstack(low_pts[chan_range]),
                      np.hstack(high_pts[chan_range]),
                      method='distrib',
                      verbose=True)

plt.grid(True)
plt.xlabel(r"ln I$_{\rm int}$ / I$_{\rm SD}$")
plt.tight_layout()
plt.savefig(allfigs_path(f"14A-235_imaging/ratio_hist_14A_vla_ebhis_chan_{chan_range.start}_{chan_range.stop}_w_weights_v3.png"))
plt.savefig(allfigs_path(f"14A-235_imaging/ratio_hist_14A_vla_ebhis_chan_{chan_range.start}_{chan_range.stop}_w_weights_v3.pdf"))

print("Factor: {0}+/-{1}".format(sc_factor_chrange, sc_err_chrange))
# Factor: 1.067082747762499+/-0.0006864143680856134
# Error still underestimated

# The >1 factor is due to some emission in the GBT data being cut-off by the
# PB limit of the VLA mosaic. The factor increases far from the systemic
# velocity, where bright HI gets cut-off (compared to the larger 14B data).
# So, despite the != 1 factor, no factor will be applied to the SD data.
# Besides, the 14B mosaic comparison gives a 1.0 factor with the GBT data.
# The tests here were for consistency and that's what we find.

plt.close()