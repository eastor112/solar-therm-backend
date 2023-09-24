import numpy as np

def sky_transmissivity(ang_theta_z, local_altitude):
    """
    Calculate the transmissivity of the atmosphere for the beam radiation.

    Parameters:
    - ang_theta_z (float): Zenith angle in degrees.
    - local_altitude (float): Local altitude in meters.

    Returns:
    - sky_transmissivity (float): Transmissivity of the atmosphere for beam radiation.
    """
    # For altitudes below 2.5 km (NOTE: For high-altitude regions)
    # ------------------------------------------------------------
    a0_prime = 0.4237 - 0.00821 * (6 - local_altitude / 1000) ** 2
    a1_prime = 0.5055 + 0.00595 * (6.5 - local_altitude / 1000) ** 2
    kk_prime = 0.2711 + 0.01858 * (2.5 - local_altitude / 1000) ** 2

    # For tropical climates (consider Trujillo as a tropical climate)
    # ----------------------------------------------------------------
    r0 = 0.95
    r1 = 0.98
    rk = 1.02

    # Calculate sky transmissivity
    # -------------------------------------
    a0 = r0 * a0_prime
    a1 = r1 * a1_prime
    kk = rk * kk_prime

    sky_transmissivity = a0 + a1 * np.exp(-kk / np.cos(np.deg2rad(np.round(ang_theta_z, 9))))  # Sky transmissivity

    return sky_transmissivity


if __name__ == '__main__':
    print(sky_transmissivity(50, 80))
