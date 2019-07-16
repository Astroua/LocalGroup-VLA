
'''
Define HI frequency once.
'''

import astropy.units as u

# (Vilardell et al. 2010)
m31_distance = 744 * u.kpc


def ang_to_phys(ang_size, distance=m31_distance):
    '''
    Convert from angular to physical scales
    '''
    return (ang_size.to(u.rad).value * distance).to(u.pc)


hi_freq = 1.42040575177 * u.GHz

co21_mass_conversion = 6.7 * (u.Msun / u.pc ** 2) / (u.K * u.km / u.s)

# Note that the top two conversions contain a 1.4x correction for He.
# So they will give the atomic mass, not the HI mass!
hi_mass_conversion = 0.0196 * (u.M_sun / u.pc ** 2) / (u.K * u.km / u.s)
hi_mass_conversion_Jy = 2.36e5 * 1.4 * (u.M_sun / u.Mpc ** 2) / (u.Jy * u.km / u.s)

# This does not have the He correction
hi_coldens_Kkms = 1.82e18 * u.cm**-2 / (u.K * u.km / u.s)
