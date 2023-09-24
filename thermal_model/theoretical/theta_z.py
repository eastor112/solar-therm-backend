import numpy as np

def zenith_angle(delta, phi, gamma, omega):
    """
    Calculate the zenith angle in degrees.

    Parameters:
    - delta (float): Declination angle in degrees.
    - phi (float): Latitude in degrees.
    - gamma (float): Azimuth angle in degrees.
    - omega (float): Hour angle in degrees.

    Returns:
    - zenith_angle (float): Zenith angle in degrees.
    """
    # Convert angles to radians
    delta_rad = np.deg2rad(delta)
    phi_rad = np.deg2rad(phi)
    omega_rad = np.deg2rad(omega)

    # Calculate the zenith angle in radians
    zenith_angle_rad = np.arccos(np.sin(delta_rad) * np.sin(phi_rad) + np.cos(delta_rad) * np.cos(phi_rad) * np.cos(omega_rad))

    # Convert the zenith angle to degrees
    zenith_angle = np.rad2deg(zenith_angle_rad)

    return zenith_angle

if __name__ == '__main__':
    print(zenith_angle(50, 69, 23, 43))
