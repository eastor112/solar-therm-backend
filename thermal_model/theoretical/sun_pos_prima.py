import numpy as np

def sun_position_prima(n_x, n_y, n_z, inclination, azimuth):
    """
    Calculate the unit vectors of the sun's position.

    Parameters:
    - n_x (float): Zenith direction variable.
    - n_y (float): East direction variable.
    - n_z (float): North direction variable.
    - inclination (float): Inclination variable in degrees.
    - azimuth (float): Azimuth variable in degrees.

    Returns:
    - nnx (float): Normal direction to the inclined plane.
    - nny (float): Direction from east to south.
    - nnz (float): Direction from north to zenith.
    """
    inclination_rad = np.deg2rad(inclination)
    azimuth_rad = np.deg2rad(azimuth)

    nnx = n_x * np.cos(inclination_rad) - (n_y * np.sin(azimuth_rad) + n_z * np.cos(azimuth_rad)) * np.sin(inclination_rad)

    nny = n_y * np.cos(azimuth_rad) - n_z * np.sin(azimuth_rad)

    nnz = n_x * np.sin(inclination_rad) + (n_y * np.sin(azimuth_rad) + n_z * np.cos(azimuth_rad)) * np.cos(inclination_rad)

    return nnx, nny, nnz

if __name__ == '__main__':
    print(sun_position_prima(50, 8, 2, 23, 12))
