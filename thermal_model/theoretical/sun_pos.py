import numpy as np

def sun_position(ang_delta, latitud_local, ang_omega):
    """
    Calculate the unit vectors of the sun's position.

    Parameters:
    - ang_delta (float): Declination variable in degrees.
    - latitud_local (float): Local latitude variable in degrees.
    - ang_omega (float): Hour angle variable in degrees.

    Returns:
    - nx (float): Direction toward the zenith.
    - ny (float): Direction toward the east.
    - nz (float): Direction toward the north.
    """
    ang_delta_rad = np.deg2rad(ang_delta)
    latitud_local_rad = np.deg2rad(latitud_local)
    ang_omega_rad = np.deg2rad(ang_omega)

    nx = np.cos(ang_delta_rad) * np.cos(latitud_local_rad) * np.cos(ang_omega_rad) + np.sin(ang_delta_rad) * np.sin(latitud_local_rad)

    ny = -np.cos(ang_delta_rad) * np.sin(ang_omega_rad)

    nz = -np.cos(ang_delta_rad) * np.sin(latitud_local_rad) * np.cos(ang_omega_rad) + np.sin(ang_delta_rad) * np.cos(latitud_local_rad)

    return nx, ny, nz

if __name__ == '__main__':
    print(sun_position(50, 8, 20))
