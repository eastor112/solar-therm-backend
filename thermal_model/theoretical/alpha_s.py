def solar_altitude_angle(theta_z):
    """
    Calculate the solar altitude angle complement of the zenith angle.

    Parameters:
    - theta_z (float): Zenith angle [deg].

    Returns:
    - solar_altitude_angle (float): Solar altitude angle complement of the zenith angle [deg].
    """
    solar_altitude_angle = 90 - theta_z  # Solar altitude angle complement of the zenith angle [deg].

    return solar_altitude_angle

if __name__ == '__main__':
    print(solar_altitude_angle(100))
