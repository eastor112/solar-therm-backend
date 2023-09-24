import numpy as np

def incidence_angle(delta, phi, beta, gamma, omega):
    """
    Calculate the incidence angle in degrees.

    Parameters:
    - delta (float): Declination angle in degrees.
    - phi (float): Latitude in degrees.
    - beta (float): Inclination in degrees.
    - gamma (float): Azimuth angle in degrees.
    - omega (float): Hour angle in degrees.

    Returns:
    - incidence_angle (float): Incidence angle in degrees.
    """
    # Convert angles to radians
    delta_rad = np.deg2rad(delta)
    phi_rad = np.deg2rad(phi)
    beta_rad = np.deg2rad(beta)
    gamma_rad = np.deg2rad(gamma)
    omega_rad = np.deg2rad(omega)

    # Calculate terms
    term1 = np.sin(delta_rad) * np.sin(phi_rad) * np.cos(beta_rad)
    term2 = np.sin(delta_rad) * np.cos(phi_rad) * np.sin(beta_rad) * np.cos(gamma_rad)
    term3 = np.cos(delta_rad) * np.cos(phi_rad) * np.cos(beta_rad) * np.cos(omega_rad)
    term4 = np.cos(delta_rad) * np.sin(phi_rad) * np.sin(beta_rad) * np.cos(gamma_rad) * np.cos(omega_rad)
    term5 = np.cos(delta_rad) * np.sin(beta_rad) * np.sin(gamma_rad) * np.sin(omega_rad)

    # Calculate the incidence angle in radians
    incidence_angle_rad = np.arccos(term1 - term2 + term3 + term4 + term5)

    # Convert the incidence angle to degrees
    incidence_angle = np.rad2deg(incidence_angle_rad)

    return incidence_angle

if __name__ == '__main__':
    print(incidence_angle(50, 70, 20, 40, 50))
