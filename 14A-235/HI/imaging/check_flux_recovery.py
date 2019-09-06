
'''
Script to compare the flux recovered in the interferometer cube, the SD cube,
and (optionally) the feathered cube.
'''

import numpy as np
from spectral_cube import (SpectralCube, OneDSpectrum,)
from spectral_cube.lower_dimensional_structures import \
    VaryingResolutionOneDSpectrum
import os
from astropy.io import fits
import astropy.units as u
import matplotlib.pyplot as plt
from pandas import DataFrame

from cube_analysis.feather_cubes import flux_recovery

from paths import (fourteenA_HI_data_path,
                   fourteenA_HI_data_wEBHIS_path,
                   ebhis_m31_HI_data_path,
                   m31_data_path,
                   allfigs_path)

from constants import hi_mass_conversion_Jy, m31_distance
from plotting_styles import default_figure, onecolumn_figure

num_cores = 4
chunk = 8

# Load the non-pb masked cube
vla_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor.fits"))

ebhis_name = ebhis_m31_HI_data_path(
                  "14A-235_items/CAR_C01_14A235_match_04kms_spectralregrid.fits")
ebhis_cube = SpectralCube.read(ebhis_name)

feathered_cube = SpectralCube.read(fourteenA_HI_data_wEBHIS_path("M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered.fits"))


pb_cube = SpectralCube.read(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.pb.fits"))

mask = np.isfinite(pb_cube[0].value)

total_vla_profile, total_ebhis_profile = \
    flux_recovery(vla_cube, ebhis_cube, mask=mask, num_cores=num_cores,
                  chunk=chunk, spec_check_kwargs={'rtol': 0.03},
                  verbose=False)
total_feathered_profile, total_ebhis_profile = \
    flux_recovery(feathered_cube, ebhis_cube, mask=mask, num_cores=num_cores,
                  chunk=chunk, spec_check_kwargs={'rtol': 0.03},
                  verbose=False)

vel_axis = vla_cube.spectral_axis.to(u.km / u.s).value

onecolumn_figure()

# Plot ratio b/w high-res to EBHIS total flux per channel
plt.plot(vel_axis, total_feathered_profile / total_ebhis_profile,
         label='VLA + EBHIS')
plt.plot(vel_axis, total_vla_profile / total_ebhis_profile, label="VLA",
         linestyle='--')
# plt.axhline(1, zorder=-1, linestyle='--', color='b', alpha=0.5)
plt.ylim([0.15, 1.5])
plt.legend(frameon=True)
plt.grid(True)
plt.ylabel("VLA-to-EBHIS Flux Ratio")
plt.xlabel("Velocity (km / s)")
plt.tight_layout()
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_ratio_v3.png"))
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_ratio_v3.pdf"))
plt.close()

# Plot the total spectra
plt.plot(vel_axis, total_ebhis_profile,
         label='EBHIS')
plt.plot(vel_axis, total_vla_profile, label="VLA",
         linestyle='--')
plt.plot(vel_axis, total_feathered_profile,
         label='VLA + EBHIS', linestyle=":")
plt.legend(frameon=True)
plt.grid(True)
# plt.ylim([-3, 70])
plt.ylabel("Total Flux (Jy)")
plt.xlabel("Velocity (km / s)")
plt.tight_layout()
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_v3.png"))
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_v3.pdf"))
plt.close()

plt.plot(vel_axis, total_ebhis_profile,
         label='EBHIS')
plt.plot(vel_axis, total_vla_profile, label="VLA",
         linestyle='--')
plt.plot(vel_axis, total_feathered_profile,
         label='VLA + EBHIS', linestyle=":")
plt.legend(frameon=True)
plt.grid(True)
plt.ylim([-3, 150])
plt.ylabel("Total Flux (Jy)")
plt.xlabel("Velocity (km / s)")
plt.tight_layout()
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_zoom_v3.png"))
plt.savefig(allfigs_path("14A-235_imaging/vla_ebhis_14A_flux_recovery_zoom_v3.pdf"))
plt.close()

# We've summed up most of the data already. How about a mass estimate?
chan_width = np.abs(vel_axis[1] - vel_axis[0]) * u.km / u.s

vla_total_flux = np.sum(total_vla_profile) * chan_width
vla_mass = hi_mass_conversion_Jy * m31_distance.to(u.Mpc)**2 * vla_total_flux

feathered_total_flux = np.sum(total_feathered_profile) * chan_width
feathered_mass = hi_mass_conversion_Jy * m31_distance.to(u.Mpc)**2 * \
    feathered_total_flux

ebhis_total_flux = np.sum(total_ebhis_profile) * chan_width
ebhis_mass = hi_mass_conversion_Jy * m31_distance.to(u.Mpc)**2 * ebhis_total_flux

print("VLA HI Total Mass: {}".format(vla_mass))
print("EBHIS HI Total Mass: {}".format(ebhis_mass))
print("VLA + EBHIS HI Total Mass: {}".format(feathered_mass))

if not os.path.exists(fourteenA_HI_data_wEBHIS_path("tables", no_check=True)):
    os.mkdir(fourteenA_HI_data_wEBHIS_path("tables", no_check=True))

df = DataFrame({"VLA Mass": [vla_mass.value],
                "EBHIS Mass": [ebhis_mass.value],
                "VLA+EBHIS Mass": [feathered_mass.value]})
df.to_csv(fourteenA_HI_data_wEBHIS_path("tables/hi_masses_nomask.csv",
                                        no_check=True))

# Save the spectra, too
spec = vla_cube[:, 0, 0]

vla_spec = VaryingResolutionOneDSpectrum(total_vla_profile,
                                         unit=u.Jy, wcs=spec.wcs,
                                         meta=spec.meta,
                                         beams=vla_cube.beams if hasattr(vla_cube, 'beams') else None)
vla_spec.write(fourteenA_HI_data_path("M31_14A_HI_contsub_width_04kms.image.pbcor.total_flux_spec.fits", no_check=True))

spec = feathered_cube[:, 0, 0]

vla_feath_spec = VaryingResolutionOneDSpectrum(total_feathered_profile,
                                               unit=u.Jy, wcs=spec.wcs,
                                               meta=spec.meta,
                                               beams=vla_cube.beams if hasattr(vla_cube, 'beams') else None)
vla_feath_spec.write(fourteenA_HI_data_wEBHIS_path("M31_14A_HI_contsub_width_04kms.image.pbcor.EBHIS_feathered.total_flux_spec.fits", no_check=True))

spec = ebhis_cube[:, 0, 0]

ebhis_spec = OneDSpectrum(total_ebhis_profile,
                          unit=u.Jy, wcs=spec.wcs,
                          meta=spec.meta,
                          beam=ebhis_cube.beam)
ebhis_spec.write(ebhis_m31_HI_data_path(
                 "14A-235_items/CAR_C01_14A235_match_04kms_spectralregrid.total_flux_spec.fits", no_check=True),
                overwrite=True)

default_figure()
