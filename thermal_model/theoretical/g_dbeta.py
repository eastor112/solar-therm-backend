import numpy as np

def diffuse_radiation_inclined_surface(Gd, inclinacion):
    """
    Calculate diffuse radiation received by an inclined surface.

    Parameters:
    - Gd (float): Diffuse horizontal radiation [W/m2].
    - inclinacion (float): Inclination angle [deg].

    Returns:
    - diffuse_radiation_inclined_surface (float): Diffuse radiation received by an inclined surface [W/m2].
    """
    diffuse_radiation_inclined_surface = 0.5 * (1 + np.cos(np.deg2rad(inclinacion))) * Gd  # Diffuse radiation received by an inclined surface [W/m2] (Tang, 2009)

    return diffuse_radiation_inclined_surface

if __name__ == '__main__':
    print(diffuse_radiation_inclined_surface(10,  3))
